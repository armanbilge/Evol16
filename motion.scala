import spire.implicits._
import spire.random.rng.MersenneTwister64
import spire.math.{Jet, JetDim}

implicit val rng = MersenneTwister64.fromTime(1)
implicit val jd = JetDim(1)

val patterns = SeqIO.parseFasta("primates.fst")
val sm = JC[Jet[Double]]
val like = new JetTreeFunctionWrapper(new TreeLikelihood[Jet[Double], Int](patterns, sm, 1.0))
val prior = ExponentialBranchPrior[Double, Int](10.0)
def post(t: Tree[Double, Int]) = {
  val (l, dL) = like(t)
  val (p, dP) = prior(t)
  (l + p, Vector.fill(4)(0.0) ++ Vector(dL.last + dP.last))
}

val ch_go = {
  val nodes = (0 until 6).toSet
  val branches = IndexedSeq(Branch(0, 4), Branch(1, 4), Branch(2, 5), Branch(3, 5), Branch(4, 5)).zipWithIndex.toMap
  val neighbors = Tree.generateNeighbors(nodes, branches.keySet)
  val lengths = IndexedSeq(0.149, 0.108, 0.123, 0.251, 0.054)
  val taxa = Map(0 -> Taxon("C"), 1 -> Taxon("H"), 2 -> Taxon("G"), 3 -> Taxon("O"))
  Tree(nodes, branches, neighbors, lengths, taxa)
}

val co_gh = ch_go.nni(4, false)
val cg_ho = ch_go.nni(4, true)

def top(t: Tree[Double, Int]) = {
  val p = t.branches.view.filter(_.incident(0)).head.getAdjacent(0)
  (t.neighbors(p) -- Set(0, 4, 5)).head match {
    case 1 => 0
    case 2 => 2
    case 3 => 1
  }
}

val HMC = {
  val M = Matrix(5)((i, j) => if (i == j) 1.0 else 0.0)
  new PhyloHMC[Double, Int](post, M, 1.0, 0.0, 0, identity[Double]) with VuLeapProg[Double, Int]
}
val q = cg_ho.modifyLengths(_.updated(4, 0.125))
val p = IndexedSeq.fill(5)(0.0)
val z = Z(q, p, HMC.U, HMC.K)
val initH = z.H
val L = 1000
val eps = 1.0 / 512.0
(0 until L).scanLeft(z)((z, _) => HMC.leapprog(eps)(z)).foreach { z =>
  val t = top(z.q)
  val theta = t * 2.0 / 3.0 * math.Pi
  val a = math.min(math.exp(initH - z.H), 1)
  println(Traversable[Any](z.q.lengths(4) * math.cos(theta), z.q.lengths(4) * math.sin(theta), z.u, t, z.q.lengths(4), a).mkString("\t"))
}

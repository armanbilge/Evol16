import spire.implicits._

val patterns = SeqIO.parseFasta("primates.fst")

val sm = JC[Double]
val like = new TreeLikelihood[Double, Int](patterns, sm, 1.0)
val prior = ExponentialBranchPrior[Double, Int](10.0).andThen(_._1)
def post(t: Tree[Double, Int]) = like(t) + prior(t)

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

def f(t: Tree[Double, Int])(x: Double) = -post(t.modifyLengths(_.updated(4, x)))

val L = 1000
(0 to L).foreach { i =>
  val x = 0.25 / L * i
  System.out.println(Traversable(x, f(ch_go)(x), f(co_gh)(x), f(cg_ho)(x)).mkString("\t"))
}
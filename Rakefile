rule '.txt' => '.scala' do |t|
  sh "java -jar phyloHMC.jar #{t.source} > #{t.name}"
end

file 'acceptance.tex' => ['acceptance.py', 'acceptance.txt'] do |t|
  sh "python3 #{t.source} > #{t.name}"
end

file 'nondiff.pdf' => 'nondiff.py' do |t|
  sh "python3 #{t.source}"
end

file 'animation.mp4' => ['animate.py', 'motion.txt', 'surface.txt'] do |t|
  sh "python3 #{t.source}"
end

rule '.pdf' => '.tex' do |t|
  2.times do
    sh "pdflatex #{t.name.pathmap('%n')}"
  end
end

file 'evol16.pdf' => ['evol16.tex', 'acceptance.tex']

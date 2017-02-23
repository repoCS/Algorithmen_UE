library("ggplot2")

vars = read.csv("r_input.csv", header=F)

png(filename="Hanoi_algorithm_comparison.png", 
    units="cm", 
    width=14, 
    height=8, 
    pointsize=50, 
    res=150)

ggplot(vars, aes(vars$V1)) + 
  geom_line(aes(y = vars$V2, colour = "Recursive")) + 
  geom_line(aes(y = vars$V3, colour = "Look up table")) +
  ylab('Time (in seconds)') + xlab('Input numbers') +
  scale_color_manual(values=c("orange", "dodgerblue1"))

invisible(dev.off())

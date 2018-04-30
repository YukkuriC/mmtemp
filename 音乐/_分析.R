library(ggplot2)

type=c('equal','pyth','pure')
name=c('十二平均律','五度相生律','纯律')

for(song in c('luv letter','Flower Dance','克罗地亚狂想曲')){
  fdata=read.csv(sprintf('%s_freq.csv',song))
  
  # 序列图
  tmp=cumsum(fdata$length)
  fdata$from=c(0,tmp[1:(length(tmp)-1)])
  fdata$to=tmp
  
  plot_seq=ggplot()+theme_bw()+theme(panel.grid.minor.y = element_blank())+
    labs(x='时间/拍',y='频率/Hz')+scale_color_hue('律制')+
    geom_hline(aes(yintercept=440))+scale_y_log10(breaks=seq(200,1200,200))
  for(i in 1:3){
    plot_seq=plot_seq+eval(parse(
      text=sprintf(
        'geom_segment(data=fdata,aes(x=from,xend=to,y=%s,yend=%s,color="%s"),alpha=0.5)',
        type[i],type[i],name[i]
      )
    ))
  }
  
  pdf(sprintf('%s_时间序列.pdf',song),10,8,family="GB1")
  print(plot_seq)
  graphics.off()
  
  # 分布图
  plot_dist=ggplot()+theme_bw()+labs(x='音程长度/音分',y='密度')+scale_color_hue('律制')
  for(i in 1:3){
    plot_dist=plot_dist+eval(parse(
      text=sprintf(
        'stat_density(aes(x=log(fdata$%s[2:nrow(fdata)]/fdata$%s[1:(nrow(fdata)-1)],2)*1200,color="%s"),alpha=0.5,bw=6,geom="line")',
        type[i],type[i],name[i]
      )
    ))
  }
  
  pdf(sprintf('%s_音程分布.pdf',song),10,8,family="GB1")
  print(plot_dist)
  graphics.off()
  
}

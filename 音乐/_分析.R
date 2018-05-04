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
    geom_hline(aes(yintercept=440))+scale_y_log10(breaks=seq(200,1200,200))+
    geom_segment(data=fdata,aes(x=from,xend=to,y=equal,yend=equal,color="十二平均律"),alpha=0.5)+
    geom_segment(data=fdata,aes(x=from,xend=to,y=pyth,yend=pyth,color="五度相生律"),alpha=0.5)+
    geom_segment(data=fdata,aes(x=from,xend=to,y=pure,yend=pure,color="纯律"),alpha=0.5)
  
  pdf(sprintf('%s_时间序列.pdf',song),7,6,family="GB1")
  print(plot_seq)
  graphics.off()
  
  # 分布图
  plot_dist=ggplot()+theme_bw()+labs(x='音程长度/音分',y='密度')+scale_color_hue('律制')+
    stat_density(aes(x=log(fdata$equal[2:nrow(fdata)]/fdata$equal[1:(nrow(fdata)-1)],2)*1200,color="十二平均律"),alpha=0.5,bw=6,geom="line")+
    stat_density(aes(x=log(fdata$pyth[2:nrow(fdata)]/fdata$pyth[1:(nrow(fdata)-1)],2)*1200,color="五度相生律"),alpha=0.5,bw=6,geom="line")+
    stat_density(aes(x=log(fdata$pure[2:nrow(fdata)]/fdata$pure[1:(nrow(fdata)-1)],2)*1200,color="纯律"),alpha=0.5,bw=6,geom="line")
  
  pdf(sprintf('%s_音程分布.pdf',song),7,6,family="GB1")
  print(plot_dist)
  graphics.off()
  
  #音分差统计
  data_count=rbind(
    cbind(
      as.data.frame(table(round(with(fdata,log(pyth/equal,2)*1200)))),
      type='五度相生律'
    ),
    cbind(
      as.data.frame(table(round(with(fdata,log(pure/equal,2)*1200)))),
      type='纯律'
    )
  )
  data_count$Var1=as.numeric(as.vector(data_count$Var1))
  
  plot_diff=ggplot(data=data_count)+theme_bw()+labs(x='与十二平均律相差/音分',y='频数')+scale_color_hue('律制')+
    geom_segment(aes(x=Var1,xend=Var1,y=0,yend=Freq,color=type))+
    geom_point(aes(x=Var1,y=Freq,color=type))
  
  pdf(sprintf('%s_音分差分布.pdf',song),7,6,family="GB1")
  print(plot_diff)
  graphics.off()
}

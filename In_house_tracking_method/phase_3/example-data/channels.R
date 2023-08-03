library( celltrackR )
library( dplyr )

argv <- commandArgs( trailingOnly = TRUE )

trackFile <- argv[1]
outFile <- argv[2]
pairFile <- argv[3]

threshold <- 15
xThreshold <- 75

# Read tracks
t <- read.tracks.csv( trackFile, sep = ",",
	time.column = 1, id.column = 4, pos.columns = c(3,2) )
	
# Normalized tracks to compute slope
tN <- normalizeTracks( t )
m <- lm( y ~ x, data = as.data.frame(tN) )
slope <- coefficients(m)[2]

# compute "corrected y" to straighten
d1 <- as.data.frame(t)
d1$ycor <- d1$y - slope*d1$x

# compute mean corrected y per cell
yMean <- d1 %>% 
	group_by( id ) %>% 
	summarise( meanY = mean( ycor ) ) %>%
	ungroup() %>%
	arrange( meanY )

ymeans <- setNames( yMean$meanY, as.character(yMean$id) )

# create channels on the go; add new channel if y of current id is too far from
# any of the previous ones.
channelY <- numeric()
for( id in yMean$id ) {
	yi <- ymeans[as.character(id)]
	if( !any( abs(yi-channelY) < threshold ) ){
		channelY <- c( channelY, yi )
	}
}

# assign each id to the channel that fits best
channels <- unname( sapply( ymeans, function(x) which.min( abs( channelY - x ) ) ) )
channels <- setNames( channels, as.character(yMean$id) )

d1$channel <- channels[as.character(d1$id)]

# to check:
# ggplot( d1, aes( x = x, y = ycor , color = as.character(channel), group = id ) ) + geom_path()

dout <- data.frame( id = as.character(yMean$id), channel = unname( channels ) )
write.csv( dout, file = outFile, quote = FALSE, row.names = FALSE )



# pairs by time to find pairs within distance
pbt <- pairsByTime( t, searchRadius = xThreshold )
pbt$channel1 <- channels[pbt$cell1]
pbt$channel2 <- channels[pbt$cell2]
pbt <- pbt %>% 
	filter( channel1 == channel2 ) %>% 
	select( t, cell1, cell2 )

# add coordinate columns
track.list <- split( d1, d1$t )
track.list <- lapply( track.list, function(x) {rownames(x) <- x$id; return(x)})

coordinates <- apply( pbt, 1, function(x){
	tt <- as.character(as.numeric(x[1]))
	c1 <- as.character(as.numeric(x[2]))
	c2 <- as.character(as.numeric(x[3]))
	pos1 <- track.list[[tt]][c1,c("x","y")]
	pos2 <- track.list[[tt]][c2,c("x","y")]
	colnames(pos1) <- c("x1","y1")
	colnames(pos2) <- c("x2","y2")
	return( cbind( pos1, pos2 ) )
}) %>% bind_rows()

pbt <- cbind( pbt, coordinates )

write.csv( pbt, file = pairFile, quote = FALSE, row.names = FALSE )


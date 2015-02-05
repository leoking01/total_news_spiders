select *, count(distinct hash) from sinanews group by hash 



select id,hash, count(distinct hash) from sinanews group by hash

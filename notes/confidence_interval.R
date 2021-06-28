ci_preposition <- function (general, valid, alpha=0.05) {
  p_valid = valid / general;
  z = qnorm(1-alpha/2);
  ci = p_valid + c(-1,1)*z*sqrt(p_valid*(1-p_valid)/n);
  return(ci);
}

tbl <- read.csv(
  file = "/home/prodotiscus/github/rsuh2021-prepositions/notes/4fields_5.csv",
  head = FALSE, sep=",", skip=1
)
# 2,3 6,7 10,11 14,15 18,19
X=matrix(cbind(tbl$V18, tbl$V19), nrow=24)
ci_column = c();
i = 1
while (i <= length(X)/2) {
  if (X[i,2] > 0) {
    ci <- binom.test(X[i,1],X[i,2])$conf.int;
    print(sprintf("%f-%f", ci[1], ci[2]));
  } else {
    print("no")
  }
  i <- i + 1;
}
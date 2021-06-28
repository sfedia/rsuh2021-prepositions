matches <- read.csv(
  file = "/home/prodotiscus/github/rsuh2021-prepositions/notes/frequency.csv",
  head = FALSE, sep=",", skip=1
  )
print(matches$V2)
numbers <- c(
  matches$V2,
  matches$V3,
  matches$V4,
  matches$V5,
  matches$V6
)
print(numbers$V2)

xy_for_row <- function (index) {
  my_row <- c(
    matches$V2[index],
    matches$V3[index],
    matches$V4[index],
    matches$V5[index],
    matches$V6[index]
  );
  sum_others <- c(
    sum(matches$V2[(-index)]),
    sum(matches$V3[(-index)]),
    sum(matches$V4[(-index)]),
    sum(matches$V5[(-index)]),
    sum(matches$V6[(-index)])
  );
  return(matrix(c(my_row, sum_others), ncol=5, byrow=T));
}

shorted_xy_for_row <- function (index, col) {
  Z = xy_for_row(index);
  return(matrix(c(
    c(Z[1,col], sum(Z[1,(1:5)[-col]])),
    c(Z[2,col], sum(Z[2,(1:5)[-col]]))
  ), ncol=2, byrow=T));
}

p_for_row <- function (i) {
  return(c(
    chisq.test(shorted_xy_for_row(i, 1))$p.value,
    chisq.test(shorted_xy_for_row(i, 2))$p.value,
    chisq.test(shorted_xy_for_row(i, 3))$p.value,
    chisq.test(shorted_xy_for_row(i, 4))$p.value,
    chisq.test(shorted_xy_for_row(i, 5))$p.value
  ));
}

p_for_row_fisher <- function (i) {
  return(c(
    fisher.test(shorted_xy_for_row(i, 1))$p.value,
    fisher.test(shorted_xy_for_row(i, 2))$p.value,
    fisher.test(shorted_xy_for_row(i, 3))$p.value,
    fisher.test(shorted_xy_for_row(i, 4))$p.value,
    fisher.test(shorted_xy_for_row(i, 5))$p.value
  ));
}

p_bool <- function (p_list, comp = 0.01/24) {
  return(c(
    p_list[1] < comp,
    p_list[2] < comp,
    p_list[3] < comp,
    p_list[4] < comp,
    p_list[5] < comp
  ));
}

bool_print <- function (comp) {
  i = 1;
  while (i <= 24) {
    print(p_bool(p_for_row_fisher(i), comp));
    i <- i + 1;
  }
}

#=============================================================
# ~/TFAT_Letter/make_letter.r
# Created: 14 Sep 2018 15:51:56
#
# DESCRIPTION:
#
#
#
# A. Cottrill
#=============================================================

args <- commandArgs(trailingOnly = TRUE)

# test if there is at least one argument: if not, return an error
if (length(args) == 0) {
  msg <- "At least one argument must be supplied (input file).n"
  stop(msg, call. = FALSE)
} else if (length(args) == 1) {
  args[2] <- 8
}

params <- list(
  "RECOVERY_EVENT" = as.numeric(args[1]),
  "ZOOM" = as.numeric(args[2])
)

today <- format(Sys.time(), "%Y-%m-%d")

output_file <- sprintf("./../../media/tag_return_letters/Event-%s_%s.docx",
                       args[1], today)

rmarkdown::render("./tfat/recovery_letter_rmd/tagreturn.Rmd",
                  params = params,
                  output_file = output_file)
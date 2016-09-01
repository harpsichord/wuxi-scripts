#!/usr/bin/gawk -f
#Author: Wu Xi
#Date: 20160901
#Purpose: Parse key values pairs to variable declaration
#         Pass the result back to bash scripts
#         Use eval to expand the variables
#Example: This script is written to parse output of 'racadm jobqueue' command

BEGIN {
  JS = 0;
  JP = 0;
}
{
n = index($i, "=");          # search for =
# if you know precisely what variable names you expect to get, you can assign to them here:
if ( $0 ~ /Status/ ) {
  vars[substr($i, 1, n - 1)] = substr($i, n + 1)
  JS = vars["Status"];
}
if ( $0 ~ /Percent/ ) {
  vars[substr($i, 1, n - 1)] = substr($i, n + 1)
  JP = vars["Percent Complete"];
}
}
END {
  print "JS='" JS"'";
  print "JP='" JP"'";
}

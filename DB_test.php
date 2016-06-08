<?php
$s=mysql_connect("localhost","root","zeng1877") or die("failed to connect DB");
print"DB connected.<BR>";
mysql_select_db("watcher",$s);
$all = mysql_query("select * from record");
while($result=mysql_fetch_array($all)){
    print $result[0];
    print "    :   ";
    print $result[1];
    echo "<img src=$result[1]>";
    print "<BR>";
}
if(mysql_close($s)){
    print "Disconnect success";
}else{
    print "Disconnect failed";
}
?>

<?php
if (isset($_GET["ip"])){
    echo "servers/".$_GET["ip"];
    file_put_contents("servers/".$_GET["ip"], "");
}

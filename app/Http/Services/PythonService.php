<?php

namespace App\Http\Services;

use Symfony\Component\Process\Process; 
use Symfony\Component\Process\Exception\ProcessFailedException;  

class PythonService{

public function main($id){


    echo shell_exec("python ./../resources/python/main.py .$id 2>&1");
    }
}


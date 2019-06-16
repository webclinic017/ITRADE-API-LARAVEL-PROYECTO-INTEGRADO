<?php

namespace App\Http\Services;

use Symfony\Component\Process\Process; 
use Symfony\Component\Process\Exception\ProcessFailedException;  

class PythonService{

public function main(){

    echo shell_exec("python ./../resources/python/main.py 2>&1");
    }
}


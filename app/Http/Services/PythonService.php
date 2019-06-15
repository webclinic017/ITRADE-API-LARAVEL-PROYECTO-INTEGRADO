<?php

namespace App\Http\Services;

use Symfony\Component\Process\Process; 
use Symfony\Component\Process\Exception\ProcessFailedException;  

class PythonService{

public function main(){

    
    //echo "tus muertos";
    
    echo shell_exec("python ./../resources/python/main.py 2>&1");

    
    }
}


    //$pythonPath = "C:\Users\MTXDevp\AppData\Local\Programs\Python\Python37-32\python.exe";
    //$path = "runas /user:MTXDevp" .resource_path().'/python/hola.py';
    
    //$path =  resource_path()."\python\hola.py";
    //echo shell_exec("python" .resource_path()."\python\hola.py");
    //print($path);

    /*
    
    $process = new Process('C:/Users/MTXDevp/Anaconda3/python' . " hola.py");
    $process->run();

    if (!$process->isSuccessful()) {     
    
        throw new ProcessFailedException($process); 
    }  

    echo $process->getOutput();
    */


    //FUNCIONA SI EL SCRIPT ESTA EN LA MISMA CARPETA---------------------------->

    //echo shell_exec("python" . "./../hola.py");

 
    /*
    $path = "hola.py";
    
    $process = new Process('python '. $path);
    $process->run();

    if (!$process->isSuccessful()) {     
    
        throw new ProcessFailedException($process); 
    }  
    echo $process->getOutput();
    }
    */

    /*
$path = public_path().'/python/stocker.py';

$process = new Process("python ", $path);
   
//$process = new Process('python3', resource_path().'/python/stocker.py'); 

$process->run();  

if (!$process->isSuccessful()) {     
    
    throw new ProcessFailedException($process); 
}  
echo $process->getOutput();
//dump(json_decode($process->getOutput(), true));
    }
}

*/
//$process = new Process('python ','./stocker.py'); 

//exec('python ./stocker.py');

//return shell_exec('python /../../../../public/python/stocker.py');



// executes after the command finishes if (!$process->isSuccessful()) {     throw new ProcessFailedException($process); }  echo $process->getOutput();


//return resource_path()."/python/stocker.py";

//return exec("python ".resource_path()."/python/stocker.py");

//return resource_path()."/python/stocker.py";





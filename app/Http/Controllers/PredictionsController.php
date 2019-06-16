<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Predictions;
use App\Http\Services\PythonService;



class PredictionsController extends Controller
{

    private $pythonService;
    
    public function __construct() { 
        
        $this->pythonService = new PythonService(); 
    }

    /**
     * Display a listing of the resource.php artisan route:list
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return $this->pythonService->main();
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    public function getFotos(Request $request){



    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $request->validate([
            'id' => 'required',
            'referencia' => 'required'
        ]);
        $pr = predictions::create($request->all());
        return response()->json([
            'message' => 'Registro insertado con éxito',
            'pr' => $pr
        ]);
        //return "referencia insertada con éxito en la base de datos";
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}

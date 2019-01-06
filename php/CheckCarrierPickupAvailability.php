<?php
require_once 'Stamps.php';

$address = $_GET['Address'];
$city = $_GET['City'];
$state = $_GET['State'];
$zip = $_GET['Zip'];


$wsdl = WSDL;

$trace = true;
$exceptions = false;

$AC = array(
'Credentials'=>array('IntegrationID' => INTEGRATIONID,'Username' => USERNAME,'Password'=>PASSWORD),
'Address'=>array('Address'=>$address,'City'=>$city,'State'=>$state,'ZIP'=>$zip)
);


$error=2;
$error_message='';
try
{
   $client = new SoapClient($wsdl, array('trace' => $trace, 'exceptions' => $exceptions));
   $response = $client->CheckCarrierPickupAvailability($AC);
   $error=0;
}

catch (Exception $e)
{
   #echo "Error!";
   $error_message = $e -> getMessage ();
   #echo 'Last response: '. $client->__getLastResponse();
   $error=1;
   header('Content-Type: application/json');
   echo '{"response":"error","error_message": "Address not found"}';
   exit();
}

if($error==0){
$PickUpDayOfWeek =$response->PickUpDayOfWeek;
$PickupDate = $response->PickupDate;

if(!empty($PickupDate)){
header('Content-Type: application/json');
echo '{"response":"ok","PickupDate": "'.$PickupDate.'", "PickUpDayOfWeek": "'.$PickUpDayOfWeek.'"}';
}else{
  header('Content-Type: application/json');
  echo '{"response":"error","error_message": "Address not found"}';
}
}else{
header('Content-Type: application/json');
echo '{"response":"error","error_message": "Address not found"}';
}

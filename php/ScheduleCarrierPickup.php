<?php

/***
* @default values for the PackageInformation
* <NumberOfExpressMailPieces>1</NumberOfExpressMailPieces>
* <NumberOfFirstClassPieces>4</NumberOfFirstClassPieces>
* <NumberOfOtherPieces>6</NumberOfOtherPieces>
* <TotalWeightOfPackagesLbs>30</TotalWeightOfPackagesLbs>
* NumberOfExpressMailPieces / NumberOfPriorityMailPieces / NumberOfInternationalPieces / NumberOfFirstClassPackagePieces
* NumberOfParcelSelectPieces /  NumberOfOtherPieces
*** SpecialInstruction ==additional info
@Default Values for PackageLocation
FrontDoor
BackDoor
SideDoor
KnockOnDoorOrRingBell
MailRoom
Office
Reception
InOrAtMailbox
Other
**/



require_once 'Stamps.php';

//UserInfo
$first_name   = $_GET['FirstName'];
$last_name    = $_GET['LastName'];
$phone_number = $_GET['PhoneNumber'];

//address
$address  = $_GET['Address'];
$city     = $_GET['City'];
$state    = $_GET['State'];
$zip      = $_GET['Zip'];

//PackageInfo
$first_class_pieces   = $_GET['first_class_pieces'];
$express_mail_pieces  = $_GET['express_mail_pieces'];
$priority_mail_pieces = $_GET['priority_mail_pieces'];
$weight_pounds        = $_GET['weight_pounds'];
$pickupLocation       = $_GET['pickupLocation'];

$additional_instructions = $_GET['additional_instructions'];

$wsdl = WSDL;




$trace = true;
$exceptions = false;

$AC = array(
'Credentials'=>array('IntegrationID' => INTEGRATIONID,'Username' => USERNAME,'Password'=>PASSWORD),
'ContactInformation'=>array('FirstName'=>$first_name,'LastName'=>$last_name,'PhoneNumber'=>$phone_number),
'Address'=>array('Address'=>$address,'City'=>$city,'State'=>$state,'ZIP'=>$zip),
'PackageInformation'=>array('NumberOfFirstClassPieces'=>$first_class_pieces,'NumberOfExpressMailPieces'=>$express_mail_pieces
,'NumberOfPriorityMailPieces'=>$priority_mail_pieces,'SpecialInstruction'=>$additional_instructions,'TotalWeightOfPackagesLbs'=>$weight_pounds,'PackageLocation'=>$pickupLocation),
'Carrier'=>'Usps'
);


$error=2;
$error_message='';

try
{
   $client = new SoapClient($wsdl, array('trace' => $trace, 'exceptions' => $exceptions));
   $response = $client->ScheduleCarrierPickup($AC);
   $error = 0;
}

catch (Exception $e)
{
   #echo "Error!";
   #$e -> getMessage ();
   #echo 'Last response: '. $client->__getLastResponse();
   $error=1;
   header('Content-Type: application/json');
   echo '{"response":"error","error_message": "Address not found1"}';
   exit();
}

if($error==0){
$PickUpDayOfWeek =$response->PickUpDayOfWeek;
$PickupDate = $response->PickupDate;
$ConfirmationNumber = $response->ConfirmationNumber;

if(!empty($PickupDate)){
header('Content-Type: application/json');
echo '{"response":"ok","PickupDate": "'.$PickupDate.'", "PickUpDayOfWeek": "'.$PickUpDayOfWeek.'" , "ConfirmationNumber": "'.$ConfirmationNumber.'"}';
}else{
  header('Content-Type: application/json');
  #echo '{"response":"error","error_message": "Address not found2"}';
  var_dump($response);
}
}else{
header('Content-Type: application/json');
echo '{"response":"error","error_message": "Address not found3"}';
}

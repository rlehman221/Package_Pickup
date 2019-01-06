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
$first_name   = "sam";
$last_name    = "b";
$phone_number = "8744883682";

//address
$address  = "60 Cranbury Neck Road";
$city     = "Cranbury";
$state    = "NJ";
$zip      = "08512";

//PackageInfo
$first_class_pieces   = "0";
$express_mail_pieces  = "0";
$priority_mail_pieces = "1";
$weight_pounds        = "1.5";
$pickupLocation       = "FrontDoor";

$additional_instructions = "careful it's Fragile";

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
   $e -> getMessage ();
   echo 'Last response: '. $client->__getLastResponse();
   $error=1;
   header('Content-Type: application/json');
   echo '{"response":"error","error_message": "Address not found1"}';
   exit();
}

var_dump($response);
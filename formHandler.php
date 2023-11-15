<?php
$name=$_POST['name'];
$visitor_email=$_POST['email'];
$field=$_POST['field'];
$message=$_POST['message'];
$email_from='gkk@sihproject.com';
$email_subject='New Form Submission';
$email_body="User Name: $name.\n".
            "User Email:$visitor_email.\n".
            "User Field: $field.\n".
            "User Message:$message.\n";
 $to='gurnamkaur8307@gamil.com';
 $headers="From: $visitor_email \r\n";           
 $headers .="Reply-To: $visitor_email \r\n";
 mail($to,$email_subject,$email_body,$headers);
 header("location:contact.html");
 ?>
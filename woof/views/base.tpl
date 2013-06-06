<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{{ get('title','Waldo') }}</title>
    <meta name="authors" content="Luis Pedro Coelho, Shannon Quinn, Hagit Shatkay, Robert F. Murphy" />
    <meta name="keywords" content="subcellular location, subcellular localization, protein, database" />
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <link rel="stylesheet" type="text/css" href="/media/css/style.css" media="screen" />
    <link rel="shortcut icon" href="favicon.ico" />
</head>


<body>
<div id="header">
<h1><a href="{{ get_url('home') }}">Waldo</a></h1>
<h2>Where Proteins Are</h2>
</div>

<div id="content">
    <div class="right">
        <ul>
        <li><a href="{{ get_url('help') }}">Help</a></li>
        <li><a href="{{ get_url('about') }}">About Waldo</a></li>
        <li><a href="{{ get_url('contact-us') }}">Contact Us</a></li>
        </ul>
    </div>
    <div id="main">
        %include
    </div>
    <div style="clear: both;"> </div>
</div>

<hr style="margin-top: 3em" />
<div class="footer">
    <p>Copyright (c) 2010-2013. Luis Pedro Coelho, Shannon Quinn, Hagit Shatkay, Robert F. Murphy, and Jephthah Liddie. All rights reserved.</p>
</div>
</body>
</html>

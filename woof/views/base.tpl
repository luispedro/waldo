<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{{ title or 'Waldo' }}</title>
    <meta name="authors" content="Luis Pedro Coelho, Shannon Quinn, Hagit Shatkay, Robert F. Murphy" />
    <meta name="keywords" content="subcellular location, subcellular localization, protein, database" />
    <script type="text/javascript" src="/media/js/jquery.js"></script>
    <link rel="stylesheet" type="text/css" href="/media/css/whitelove.css" media="screen" />
    <link rel="shortcut icon" href="favicon.ico" />
</head>


<body>
<div id="header">
<h1><a href="{% url home %}">Waldo</a></h1>
<h2>Where Proteins Are</h2>
</div>

{% autoescape off %}
        <div id="content">
            <div class="left">
                %include
            </div>
            <div class="right">
                <ul>
                <li><a href="{% url help %}">Help</a></li>
                <li><a href="{% url about %}">About Waldo</a></li>
                <li><a href="{% url contact-us %}">Contact Us</a></li>
                </ul>
            </div>
            <div style="clear: both;"> </div>
        </div>
{% endautoescape %}

<hr style="margin-top: 3em" />
<div class="footer">
    <p>Copyright (c) 2010-2012. Luis Pedro Coelho, Shannon Quinn, Hagit Shatkay, Robert F. Murphy, and Jephthah Liddie. All rights reserved.</p>
    <p>Website CSS by <a href="http://www.free-css-templates.com/">Free CSS Templates</a>, Thanks to <a href="http://www.dubaiapartments.biz/hotels/">Hotels - Dubai</a>.</p>
</div>
</body>
</html>

<h2>Contact Us</h2>

<p>Please use one of the following email addresses for questions/comments about
waldo:</p>

<script>
function build_address(username, hostname) {
    var full = username + '@' + hostname;
    document.write('<a href="mailto:'+full+'">'+full+'</a>');
}
</script>
<ul>
    <li><script>build_address('luis','luispedro.org')</script></li>
    <li><script>build_address('murphy','cmu.edu')</script></li>
</ul>

%rebase base title='Contact Us'


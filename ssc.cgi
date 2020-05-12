#!/usr/bin/perl -w

use strict;
# Dependencies ###################################
use FileHandle qw();
use File::Basename qw();
use Cwd qw();
my $base_dir;
my $relative_path;
BEGIN {
   $relative_path = './';
   $base_dir = Cwd::realpath(File::Basename::dirname(__FILE__) . '/' . $relative_path);
}
# Dependencies ####################################
use lib "$base_dir/lib64/perl5";
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser) ;
use YAML::XS qw(LoadFile Load);
##################################################

# Version Info ###################################
my $VERSION = "1.0.0";
##################################################

#################
# Config Values #
#################
my $CONFIG_FILE = "$base_dir/resources/sscconf.yml";

package SSC;
sub new {
	my $class = shift;
	my $web_url = shift;
	my $self = {};
    $self->{web_url} = $web_url;
	return bless $self;
}

sub trimwhitespace {
	my $self = shift;
	my $stringtotrim = shift;

	$stringtotrim =~ s/^\s+//g;
	$stringtotrim =~ s/\s+$//g;

	return $stringtotrim;
}

# Display Methods ########################################################
sub displayerror {
	my $self = shift;
	my $message = shift;
	print <<MESSAGE
	<p>Error: $message</p>
MESSAGE
}
sub displayheader {
	my $self = shift;
	my $title = shift;
	my $menu_font = shift;
    my $mode = shift;

print <<HEADER;
<!DOCTYPE html>
<html>
<head>
   <title>$title</title>
   <meta charset="iso-8859-1">
   <meta name="viewport" content="width=device-width, initial-scale=1">
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <link rel='stylesheet' href='//code.jquery.com/ui/1.12.1/themes/dark-hive/jquery-ui.css'>
   <style type="text/css">

   body {
      background-color: #fff;
	  padding: 0;
	  margin: 0;
   }

   div.outer {
HEADER
;;
	if ($mode ne "nav") {
     print "min-height: 400px;";
    }
   print <<MIDHEADER;
     min-width: 326px;  
   }
   span#title-text {
      color: #fff;
      font-size: 24pt;
	  font-family: Verdana, Arial, Helvetica, sans-serif;
      font-weight: bold;
	  padding: 0 10px 0 10px; 
   }

   div#home-button {
      float: right;
   }
   div.header-row {
     background-color: #214888;
     color: #fff;
      width: 100%;
      display: block;
      float: left;
      border: 1px dotted green;
   }
   div.header-row a {
     color: #fff;
	 padding: 0 10px 0 10px; 
   }

   div#menurow {
     background-color: #000;
     visibility: hidden;
   } 

   form {
	  padding: 10px;
   }
   input, label {
      margin: 3px;
      padding: 3px 10px 5px 10px;
   }
   label {
	  width: 75px;
      font-weight: bold;
	  text-align: right;
   }
   input {
	  border-radius: 6px;     
   }
   input.text,
   input.number,
   input.list {
      width: 50px;
   }
   input.date {
      width: 80px;
   }
   input.text {
      text-align: left;
   }
   input.number {
	  text-align: right;
   }
   .column-label {
      padding: 2px 5px 2px 5px;
	  border: 2px solid #aaa;
   }

   td {
      margin: 0;
   }

   th {
	  font-family: Verdana, Arial, Helvetica, sans-serif;
	  padding: 2px 10px 2px 10px;
   }
   tr {
	  white-space: nowrap;
   }
   p.error {
	  color: #f00;
   }

   table.display-table {
      border-right: 1px solid #eee;
   }
   table.display-table td {
      border-left: 1px solid #eee;
	  border-bottom: 1px solid #eee;
   }

   a:hover {
      font-weight: bold;
   }
   a, a:visited {
	   color: #4286f4;
   }

   a#glossary_button:hover {
      text-decoration: underline;
	  cursor: pointer
   }

   td.query-field input {
	  width: 275px;
   }

   td {
      font-size: 12pt;
	  font-family: Arial, Helvetica, sans-serif;
   }

   tr.even-row {
      background-color: #eee;
   }

   tr.odd-row {
      background-color: #fff;
   }

   td#stat-graph-col {
      background-color: #fefefe;
   }
   td.edit-box {
      text-align: center;
      white-space: nowrap;
   }
   td.edit-box input {
	  margin: 0 10px 0 15px;
   }
   td.edit-box label {
	  text-align: left;
   }
   div#logout-button {
      float: right;
      margin: 0 25px 0 25px;
   }
   
   div.report {
	  font-family: 11pt monospace, sans-serif;
	  border: 1px solid #eee;
	  background-color: #f6f8fa;
   }

   .bold-text {
      font-weight: bold;
   }

   input.execute-button {
	  min-width: 90px;
   }

   .ui-menu-item-wrapper {
     font-size: $menu_font !important;
   }

   .ui-menu-icons .ui-menu-item-wrapper {
     padding-left: .5em;
   }

   	h1,h2,h3 {
	  text-align:left;
	}
	h1, h2, h3 {
	  margin:5px;
	}
	section {
	  # width:90%;
	  padding: 3px; 
	  height: auto;
	  column-count:2;
	  margin: auto;
	}

	.h2_box {
		# border-radius: 10px;
		background: grey;
		# margin: 10px;
		border-color: black;
		border: solid black;
	}

	a {
	  # text-decoration:none;
	  color:blue;
	  font-size:12px;
	}
	dl {
	  	border-radius: 10px;
		border-color: black;
		border: solid black;
		padding: 3px;
		overflow: hidden;
	}
	dt {
		padding: 1px;
	}
	dt::before {content: '✓'; margin: 2px;}
   </style>
   <script>
		function getCookie(key) {
            var keyValue = document.cookie.match("(^|;) ?" + key + "=([^;]*)(;|\$)");
            return keyValue ? keyValue[2] : null;
        }

		function setCookie(key, value) {
      	    var expires = new Date();
        	expires.setTime(expires.getTime() + 1000);
        	document.cookie = key + '=' + value + ';expires=' + expires.toUTCString();
      	}
   </script>
</head>
<body>
<div class="outer">
      <div class='header-row'>
          <span id="title-text">$title</span>
      </div>
MIDHEADER
;
}

sub setBodyMenu {
	my $self = shift;
	my @menu = shift;

	my $menu_list = $menu[0];

	if( @menu ) {
		print "<section>";

		foreach my $sec ( @$menu_list ) {
			print "<dl>";
			print "<h3 class='h2_box'>$sec->{'box-name'}</h3>";

			if( $sec->{'box-type'} =~ /menu/i ) {
				my $items = $sec->{'box-items'};
				if ( scalar @$items ) {
					foreach my $item ( @$items ) {
						if ( $item->{'box-type'} =~ /menu/i ) {
							print "<h4>$item->{'box-name'}</h4>";
							my $submenu = $item->{'box-items'};
							if ( scalar @$submenu ) {
								
								foreach my $subitem ( @$submenu ) {
									
									if ( $subitem->{'box-type'} =~ /menu/i ) {
										print "<h4>$subitem->{'box-name'}</h4>";
									}
									elsif( $subitem->{'box-type'} =~ /link/i ) {
										
										if (lc $subitem->{'newwindow'} eq "yes") {
											print "<dt><a href='$subitem->{url}' target='_blank'>$subitem->{'box-name'}</a></dt>";
										} else {
											print "<dt><a href='$subitem->{url}'>$subitem->{'box-name'}</a></dt>";
										}
									}
								}
								
							}
						}
						elsif( $item->{'box-type'} =~ /link/i ) {
							
							if (lc $item->{'newwindow'} eq "yes") {
								print "<dt><a href='$item->{url}' target='_blank'>$item->{'box-name'}</a></dt>";
							} else {
								print "<dt><a href='$item->{url}'>$item->{'box-name'}</a></dt>";
							}
							
						}
					}
				}
			}
			elsif( $sec->{'box-type'} =~ /link/i ) {
				my $items = $sec->{'box-items'};
				if ( scalar @$items ) {
					foreach my $item ( @$items ) {
						if (lc $item->{'newwindow'} eq "yes") {
							print "<dt><a href='$item->{url}' target='_blank'>$item->{'box-name'}</a></dt>";
						} else {
							print "<dt><a href='$item->{url}'>$item->{'box-name'}</a></dt>";
						}
					}
				}
			}

			print "</dl>";
		}
		print "</section>";
	}
}

sub displaymenusection {
	my $self = shift;
	my @menu = shift;

	print <<MENUHEADER
    <script src='https://code.jquery.com/jquery-1.12.4.js'></script>
	<script src='https://code.jquery.com/ui/1.12.1/jquery-ui.js'></script>
	<div id='menurow'>
    <table><tr>
MENUHEADER
;

	my $depth = 0;
	$self->displaymenu(\@menu, $depth);
	
	print <<MENUEND
    </tr></table>
	</div>
	<script>
		jQuery("ul.ssc-menu").each(function () {
			jQuery(this).menu();
            jQuery(this).menu("option", "position", { my: "left top", at: "center bottom"});
		})
		jQuery("div#menurow").css("visibility","visible");
	</script>
MENUEND
;	
}

sub displaymenu {
	my $self = shift;
	my $menu_ptr = shift;
	my @menu = @{$menu_ptr};
	my $depth = shift;

	my $listcount = 0;
	my $listmax = 0;
	while (my $menu_item = $menu[0][$listmax]) {
		$listmax++;
	}
	while (my $menu_item = $menu[0][$listcount]) {
		my $item_name = $menu_item->{name} ;
		my $item_type = $menu_item->{type};
		#$item_name = "$item_name $depth $listcount $listmax";
		if (lc $item_type eq 'menu') {
			my @menuitems = $menu_item->{items};
			if ($depth == 0) {
				print "<td><ul class='ssc-menu'>\n";
				print "<li><div>$item_name</div>\n";
				$self->displaymenu(\@menuitems, $depth + 1);
				print "</li>\n";
				print "</ul></td>\n";
			} else {
                if ($listcount == 0) {
					print "<ul class='ssc-menu'>\n";
                }
				print "<li><div>$item_name</div>\n";
				$self->displaymenu(\@menuitems, $depth + 1);
				print "</li>\n";

				if ($listcount == $listmax-1) {
					print "</ul>\n";
				}
			}
		} elsif (lc $item_type eq 'link') {
			my $link = $menu_item->{url};
			my $newwindow = $menu_item->{newwindow};
			if ($depth == 0) {
				print "<ul class='ssc-menu'>\n";
				if (lc $newwindow eq "yes") {
					print "<li><div><a href='$link' target='_blank'>$item_name</a></div></li>\n";
				} else {
					print "<li><div><a href='$link'>$item_name</a></div></li>\n";
				}
				print "</ul>\n";
			} else {
                if ($listcount == 0) {	
					print "<ul>\n";
				}
				if (lc $newwindow eq "yes") {
					print "<li><div><a href='$link' target='_blank'>$item_name</a></div></li>\n";
				} else {
					print "<li><div><a href='$link'>$item_name</a></div></li>\n";
				}
				if ($listcount == $listmax-1) {
					print "</ul>\n";
				}
			}
		}
		$listcount++;
	}
}


sub getYearFromString {
	my $self = shift;
	my $datestr = shift;

	my $yearstr = $datestr;
	$yearstr =~ s/-\d\d-\d\d\s\d\d:\d\d$//g;

	return $yearstr;
}
sub getMonthFromString {
	my $self = shift;
	my $datestr = shift;

	my $monthstr = $datestr;	
	$monthstr =~ s/-\d\d\s\d\d:\d\d$//g;	
	$monthstr =~ s/^\d\d\d\d-//g;

	return $monthstr;
}
sub getDayFromString {
	my $self = shift;
	my $datestr = shift;
	
	my $daystr = $datestr;
	$daystr =~ s/\s\d\d:\d\d$//g;
	$daystr =~ s/^\d\d\d\d-\d\d-//g;
	
	return $daystr;
}
sub getHourFromString {
	my $self = shift;
	my $datestr = shift;

	my $hourstr = $datestr;
	$hourstr =~ s/:\d\d$//g;
	$hourstr =~ s/^\d\d\d\d-\d\d-\d\d\s//g;

	return $hourstr;
}
sub getMinuteFromString {
	my $self = shift;
	my $datestr = shift;

	my $minutestr = $datestr;
	$minutestr =~ s/$//g;
	$minutestr =~ s/^\d\d\d\d-\d\d-\d\d\s\d\d://g;

	return $minutestr;
}

sub displayfooter {
	my $self = shift;
	my $footer = shift;
	print <<EOL
    </div>
	<div id='status-footer'></div>
    <div style='width: 100%; border-bottom: 1px solid #eee'></div>
	<p style='margin: 5px 10px 0 10px;color: $footer->{color};font-weight: $footer->{style}; font-size: $footer->{size}'>$footer->{text}</p>
</body>
</html>
EOL
}

###########################################################################
package main;

my $q = CGI->new;

# Load Config Data #######################################	
my $filedata = YAML::XS::LoadFile($CONFIG_FILE);
my $header_text = $filedata->{header_title};
my $fontsizemenu = $filedata->{font_size_menu};
my @menu = $filedata->{menu};
my @bodyMenu = $filedata->{'body-menu'};
my $footer_text = $filedata->{footer};
#########################################################

my $my_url = $q->url( -relative => 1 );
my @args = $q->param;
my $sscapp = SSC->new($my_url);

print $q->header(-type => 'text/html', -charset => 'utf-8');
my $mode = $q->param('mode');
$sscapp->displayheader($header_text, $fontsizemenu, $mode);
$sscapp->displaymenusection(@menu);
$sscapp->setBodyMenu(@bodyMenu);
if ($mode ne "nav") {
	$sscapp->displayfooter($footer_text);
}


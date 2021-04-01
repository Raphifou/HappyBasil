<!DOCTYPE html>
<html>

    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="style.css" />
        <title>HapPy Basil</title>
    </head>
    
    <body>
	
	<?php

		$hostname = "192.168.0.23";
		$username = "happybasil";
		$password = "g8aXq8EN;";
		$db = "data";

		$dbconnect=mysqli_connect($hostname,$username,$password,$db);

		if ($dbconnect->connect_error) {
		  die("Database connection failed: " . $dbconnect->connect_error);
		}

	?>
	
        <div id="bloc_page">
            <header>
                <div id="titre_principal">
                    <div id="logo">
                        <img src="images/ico_plant.png" alt="Logo de plante" />
                        <h1>HapPy Basil</h1>    
                    </div>
                    <h2>A plant monitoring solution based on RPi, GrovePi and Python using a web interface</h2>
                </div>
                
                <nav>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="#">Graphs</a></li>
                        <li><a href="https://github.com/Raphifou/HappyBasil">Download</a></li>
                    </ul>
                </nav>
            </header>
            
            <div id="banniere_image">
                <div id="banniere_description">
                    
					<li>MODE 	: 	? </a></li>
                    <li>LIGHT 	: 	? </a></li>
                    <li>PUMP 	:  	? </a></li>
                    
                    <a href="#" class="bouton_rouge">Update data <img src="images/flecheblanchedroite.png" alt="" /></a>
                </div>
            </div>
			
            <h1><img src="images/garden_status.png" alt="Sensors" class="ico_categorie" />SENSORS VALUE</h1>

            <div id = "garden_status">
				
                <table>
						<tr>
						<td id="light">
							<p><img src="images/sun.png" alt="Sun" /> Luminosity: ?</p>
						</td>
						<td id="temp">
							<p><img src="images/thermo.png" alt="Thermometer" /> Temperature: ?</p>
						</td>
						</tr>
						<tr>
						<td id="humidity">
							<p><img src="images/fog.png" alt="Fog" /> Humidity: ?</p>
						</td>
						<td id="moisture">
							<p><img src="images/humidity.png" alt="Drop" /> Moisture: ?</p>
						</td>
						</tr>
						<?php

						$query = mysqli_query($dbconnect, "SELECT * FROM user_review")
						   or die (mysqli_error($dbconnect));

						while ($row = mysqli_fetch_array($query)) {
						  echo
						   "<tr>
							<td>{$row['light']}</td>
							<td>{$row['temp']}</td>
							</tr>
							<tr>
							<td>{$row['humidity']}</td>
							<td>{$row['temp']}</td>
						   </tr>\n";
						}
						?>
                </table>
				<aside>
					<h1 id = "h1_aside">Garden Status & Control Panel</h1>
					<div id = "health_status"><img id="health_status" src="images/happy.png" alt="Smiley" /></div>
					<div id = "my_buttons">
					<input class="styled" type="button" value="AUTO">
					<input class="styled" type="button" value="MANUAL">
					<input class="styled" type="button" value="LIGHT">
					<input class="styled" type="button" value="PUMP">
					<input class="styled" type="button" value="OFF">
					</div>
				</aside>
			</div>
    
            <footer>
                <div id="update">
                    <h1>LAST UPDATES</h1>
                    <p>Date : xx/xx/xx</p>
                    <p>Time : xx:xx:xx</p>
                </div>
                <div id="mes_photos">
                    <h1>My garden:</h1>
                    <p><img src="images/photo1.jpg" alt="Photographie" /><img src="images/photo2.jpg" alt="Photographie" /><img src="images/photo3.jpg" alt="Photographie" /></p>
                </div>
                <div id="links">
                    <h1>Links</h1>
                    <div id="links_list">
                        <ul>
                            <li><a href="#">RaspberryPi</a></li>
                            <li><a href="#">Dexter Industries</a></li>
                            <li><a href="#">Adafruit</a></li>
                            <li><a href="#">LAMP</a></li>
                        </ul>
                        <ul>
                            <li><a href="https://mariadb.org/">MariaDB</a></li>
                            <li>Icon by <a href="https://freeicons.io/profile/3063">Oscar EstMont</a> on <a href="https://freeicons.io">freeicons.io</a></li>
                            <li>Icon by <a href="https://freeicons.io/profile/823">Muhammad Haq</a> on <a href="https://freeicons.io">freeicons.io</a></li>
                            <li>Icon by <a href="https://freeicons.io/profile/6200">Soni Sokell</a> on <a href="https://freeicons.io">freeicons.io</a></li>
                        </ul>
                    </div>
                </div>
            </footer>
        </div>
    </body>
</html>

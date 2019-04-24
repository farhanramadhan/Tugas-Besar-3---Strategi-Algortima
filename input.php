<?php
    #Untuk Memulai Session Baru
    session_start();
?>

<!DOCTYPE html>
<html>
    <head>
        <!-- Menyambungkan dengan CSS -->
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>FarcunGaming ChatBot</title>
        <link rel = "stylesheet" type = "text/css" href = "style.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <!-- Icon Website -->
        <link rel="apple-touch-icon" sizes="57x57" href="/apple-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60" href="/apple-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72" href="/apple-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76" href="/apple-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="/apple-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="/apple-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="/apple-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="/apple-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-icon-180x180.png">
        <link rel="icon" type="image/png" sizes="192x192"  href="/android-icon-192x192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
        <link rel="manifest" href="/manifest.json">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="/ms-icon-144x144.png">
        <meta name="theme-color" content="#ffffff">
    </head>

    <!-- Body dari HTML -->
    <body>
        <!-- Judul -->
        <div class = "Judul">
            <h1>FarcunGaming Chat Bot</h1>
        </div>

        <div class = "Avatar">
            <img src = "img/giphy.gif">
        </div>

        <!-- Inisiasi Chatbox -->
        <div class ="chatbox">
            <!-- Inisiasi Chatlogs -->
            <div class = "chatlogs">
                <!-- PHP yang menhubungkan antara UI dengan Backend -->
                <?php
                    #Validasi apakah session sudah pernah dibuat
                    #Jika Ya, Maka tidak masuk ke block ini
                    #JIka Tidak, Maka akan menjalankan block ini
                    if(!isset($_SESSION["Sesi"])){
                        $_SESSION["Sesi"] = array();
                        $opening = "Hello, My Name is FarcunGamingBot";
                        array_push($_SESSION['Sesi'], $opening);
                        $_SESSION["X"] = $pastString;
                    }
                    #Untuk Validasi Inputan Tidak Bisa Berulang Langsung
                    if($_POST['userInput'] == $_SESSION['X']){
                        unset($_POST['userInput']);
                        unset($_SESSION['X']);
                    }
                    #Validasi Apakah Inputan Merupakan String Kosong
                    if(strlen($_POST["userInput"]) > 0){
                        if($_POST['userInput'] != " "){
                            $chat_past = $_POST['userInput'];
                            array_push($_SESSION["Sesi"], $chat_past);
                            $stringPil = 'py '.$_POST['pilihan'].'.py';
                            $output_bot = shell_exec($stringPil.' "'.$chat_past.'"');
                            array_push($_SESSION["Sesi"], $output_bot);
                            $_SESSION["X"] = $chat_past;
                        }
                    }
                ?>
                <!-- Pembentukan Bubble Chat -->
                <?php
                    #Chat akan disimpan ke dalam sebuah Array dan akan dicetak sesuai dengan urutan yang ada
                    $i = 0;
                    #Validasi apakah array ada isinya atau tidak
                    if(count($_SESSION["Sesi"]) > 0){
                        #Penulisan semua chat yang tersimpan dalam array
                        foreach($_SESSION["Sesi"] as $x){
                            if($i == 0){
                                #Mengabungkan String dengan Bubble Chat [BOT]
                                echo '<div class = "chat bot">
                                <div class = "user-photo"><img src="img/bot1.jpg"></div>
                                <p class = "chatm">'.$x.'</p>
                                </div>';
                                echo "<br>";
                            }
                            elseif($i % 2 == 1){
                                #Mengabungkan String dengan Bubble Chat [USER]
                                echo '<div class = "chat user">
                                <div class = "user-photo"><img src="img/user1.jpeg"></div>
                                <p class = "chatm">'.$x.'</p>
                                </div>';
                                echo "<br>"; 
                            }
                            else{
                                #Mengabungkan String dengan Bubble Chat [BOT]
                                echo '<div class = "chat bot">
                                <div class = "user-photo"><img src="img/bot1.jpg"></div>
                                <p class = "chatm">'.$x.'</p>
                                </div>';
                                echo "<br>";
                            }
                            $i++;
                        }
                    }
                ?>
            </div>
            
            <!-- Membuat Form yang berisi textbox dan radio button untuk proses input -->
            <form action = "<?php $_PHP_SELF ?>" method = "POST"  onsubmit="show()">
                <!-- Textbox -->
                <div class = "input">
                    <input type = "text" name = "userInput" class = "input1">
                </div>
                
                <!-- Radio Button -->
                <div class = "radio">
                    <label class="container">Knuth Morris Pratt
                        <input type="radio" checked="checked" value="KMPMain" name="pilihan">
                        <span class="checkmark"></span>
                    </label>
                    <label class="container">Boyer-Moore
                        <input type="radio" name="pilihan" value="BMMain">
                        <span class="checkmark"></span>
                    </label>
                    <label class="container">Regular Expression
                        <input type="radio" name="pilihan" value="RegexMain">
                        <span class="checkmark"></span>
                    </label>
                </div>
                
                
                <!-- Tombol Send -->
                <div class = "button1">
                    <button class="btn1 waves-effect waves-light" type="submit" type = "button" name="action">
                        <i class="btn3">Send</i>
                    </button>
                </div>

                <script type = "text/javascript">

                function show() {
                    document.getElementById("myDiv").style.display="block";
                    setTimeout("hide()", 2000);  // 5 seconds
                }

                function hide() {
                    document.getElementById("myDiv").style.display="none";
                }

                </script>
                
            </form>
        </div>

        <!-- Button yang akan men-direct user ke Akun Youtube -->
        <form action="https://youtu.be/PTDDKQmPWtI">
            <button class="btn"><i class="fa fa-home"></i> Support The Channel</button>
        </form>
    </body>
</html>
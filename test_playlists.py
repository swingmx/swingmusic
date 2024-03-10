import requests
import random

def send_post_request():
    url = "http://localhost:1980/playlist/import"
    data = {
        'name': f'{random.randint(0,1000)}test',
        'data': """#EXTM3U
#EXTINF:214,Gryffin; Maia Wright - Body Back (feat. Maia Wright)
Gryffin - Body Back (feat. Maia Wright).mp3
#EXTINF:205,5 Seconds of Summer - Teeth
5 Seconds of Summer - Teeth.mp3
#EXTINF:180,BLACKPINK - How You Like That
BLACKPINK - How You Like That.mp3
#EXTINF:187,K-391; Alan Walker; Ahrix - End of Time
K-391 - End of Time.mp3
#EXTINF:165,Tom Santa - On & On
Tom Santa - On & On.mp3
#EXTINF:187,Charlie Puth - Light Switch
Charlie Puth - Light Switch.mp3
#EXTINF:228,Sly Chaos; NÜ - Right Now
Sly Chaos - Right Now.mp3
#EXTINF:209,The Chainsmokers; ILLENIUM; Lennon Stella - Takeaway
The Chainsmokers - Takeaway.mp3
#EXTINF:198,HEARTSTEEL; League of Legends; BAEKHYUN; tobi lou; ØZI; Cal Scruby - PARANOIA
HEARTSTEEL - PARANOIA.mp3
#EXTINF:299,Willaris. K; jamesjamesjames - Bullet Train To Paris
Willaris. K - Bullet Train To Paris.mp3
#EXTINF:207,NOTD; Astrid S - I Don't Know Why
NOTD - I Don't Know Why.mp3
#EXTINF:172,Marshmello; Halsey - Be Kind (with Halsey)
Marshmello - Be Kind (with Halsey).mp3
#EXTINF:217,The Chainsmokers; Bebe Rexha - Call You Mine
The Chainsmokers - Call You Mine.mp3
#EXTINF:189,Alan Walker - The Drum
Alan Walker - The Drum.mp3
#EXTINF:209,Duke Dumont; Nathan Nicholson - Losing Control (feat. Nathan Nicholson)
Duke Dumont - Losing Control (feat. Nathan Nicholson).mp3
#EXTINF:193,Maggie Lindemann; Cheat Codes; CADE - Pretty Girl - Cheat Codes X CADE Remix
Maggie Lindemann - Pretty Girl - Cheat Codes X CADE Remix.mp3
#EXTINF:141,The Kid LAROI; Justin Bieber - STAY (with Justin Bieber)
The Kid LAROI - STAY (with Justin Bieber).mp3
#EXTINF:184,Zedd; Maren Morris; Grey - The Middle
Zedd - The Middle.mp3
#EXTINF:184,Alan Walker; Ruben - Heading Home
Alan Walker - Heading Home.mp3
#EXTINF:182,Stray Kids - LALALALA
Stray Kids - LALALALA.mp3
#EXTINF:175,The Chainsmokers - High
The Chainsmokers - High.mp3
#EXTINF:182,FISHER; Kita Alexander - Atmosphere
FISHER - Atmosphere.mp3
#EXTINF:163,Nicky Youre; dazy - Sunroof
Nicky Youre - Sunroof.mp3
#EXTINF:153,Justin Bieber - Ghost
Justin Bieber - Ghost.mp3
#EXTINF:141,R3HAB; HRVY - Be Okay (with HRVY)
R3HAB - Be Okay (with HRVY).mp3
#EXTINF:224,Gryffin; Jason Ross; Calle Lehmann - After You (feat. Calle Lehmann)
Gryffin - After You (feat. Calle Lehmann).mp3
#EXTINF:183,Alan Walker; K-391; Boy In Space - Paradise
Alan Walker - Paradise.mp3
#EXTINF:199,Shawn Mendes - There's Nothing Holdin' Me Back
Shawn Mendes - There's Nothing Holdin' Me Back.mp3
#EXTINF:185,The Chainsmokers - I Love U
The Chainsmokers - I Love U.mp3
#EXTINF:177,Kal Elle; Nick Saady - In the Night
Kal Elle - In the Night.mp3
#EXTINF:162,Ava Max - Kings & Queens
Ava Max - Kings & Queens.mp3
#EXTINF:210,Zedd; Kehlani - Good Thing (with Kehlani)
Zedd - Good Thing (with Kehlani).mp3
#EXTINF:219,Taylor Swift - I Knew You Were Trouble.
Taylor Swift - I Knew You Were Trouble..mp3
#EXTINF:204,Hailee Steinfeld - Most Girls
Hailee Steinfeld - Most Girls.mp3
#EXTINF:203,5 Seconds of Summer - Youngblood
5 Seconds of Summer - Youngblood.mp3
#EXTINF:158,OneRepublic - Rescue Me
OneRepublic - Rescue Me.mp3
#EXTINF:210,Lil Nas X - STAR WALKIN' (League of Legends Worlds Anthem)
Lil Nas X - STAR WALKIN' (League of Legends Worlds Anthem).mp3
#EXTINF:231,Taylor Swift - Blank Space
Taylor Swift - Blank Space.mp3
#EXTINF:203,Dua Lipa - Levitating
Dua Lipa - Levitating.mp3
#EXTINF:172,Ariana Grande - positions
Ariana Grande - positions.mp3
#EXTINF:201,Jung Kook; Jack Harlow - 3D (feat. Jack Harlow)
Jung Kook - 3D (feat. Jack Harlow).mp3
#EXTINF:170,Justin Bieber - Hold On
Justin Bieber - Hold On.mp3
#EXTINF:174,Hailee Steinfeld; Alesso; Florida Georgia Line; WATT - Let Me Go (with Alesso, Florida Georgia Line & watt)
Hailee Steinfeld - Let Me Go (with Alesso, Florida Georgia Line & watt).mp3
#EXTINF:169,OneRepublic - Run
OneRepublic - Run.mp3
#EXTINF:215,Kygo; Sasha Alex Sloan - I'll Wait
Kygo - I'll Wait.mp3
#EXTINF:184,Elley Duhé - MIDDLE OF THE NIGHT
Elley Duhé - MIDDLE OF THE NIGHT.mp3
#EXTINF:207,Tate McRae - she's all i wanna be
Tate McRae - she's all i wanna be.mp3
#EXTINF:181,Hailee Steinfeld; Grey; Zedd - Starving
Hailee Steinfeld - Starving.mp3
#EXTINF:178,Alan Walker; Benjamin Ingrosso - Man On The Moon
Alan Walker - Man On The Moon.mp3
#EXTINF:231,Taylor Swift - Style
Taylor Swift - Style.mp3
#EXTINF:183,Galantis; David Guetta; Little Mix - Heartbreak Anthem (with David Guetta & Little Mix)
Galantis - Heartbreak Anthem (with David Guetta & Little Mix).mp3
#EXTINF:237,Jaymes Young - Infinity
Jaymes Young - Infinity.mp3
#EXTINF:220,Alesso; Liam Payne - Midnight (feat. Liam Payne)
Alesso - Midnight (feat. Liam Payne).mp3
#EXTINF:207,Ed Sheeran - Shivers
Ed Sheeran - Shivers.mp3
#EXTINF:182,Lady Gaga; Ariana Grande - Rain On Me (with Ariana Grande)
Lady Gaga - Rain On Me (with Ariana Grande).mp3
#EXTINF:148,OneRepublic - I Ain't Worried
OneRepublic - I Ain't Worried.mp3
#EXTINF:197,NOTD; Bea Miller - I Wanna Know (feat. Bea Miller)
NOTD - I Wanna Know (feat. Bea Miller).mp3
#EXTINF:178,Clean Bandit; Mabel; 24kGoldn - Tick Tock (feat. 24kGoldn)
Clean Bandit - Tick Tock (feat. 24kGoldn).mp3
#EXTINF:219,Taylor Swift - Shake It Off
Taylor Swift - Shake It Off.mp3
#EXTINF:174,Ava Max - My Head & My Heart
Ava Max - My Head & My Heart.mp3
#EXTINF:174,Sam Feldt; RANI - Post Malone (feat. RANI)
Sam Feldt - Post Malone (feat. RANI).mp3
#EXTINF:201,Megan Thee Stallion; Dua Lipa - Sweetest Pie
Megan Thee Stallion - Sweetest Pie.mp3
#EXTINF:140,24kGoldn; iann dior - Mood (feat. iann dior)
24kGoldn - Mood (feat. iann dior).mp3
#EXTINF:138,Alan Walker; Imanbek - Sweet Dreams
Alan Walker - Sweet Dreams.mp3
#EXTINF:178,Olivia Rodrigo - good 4 u
Olivia Rodrigo - good 4 u.mp3
#EXTINF:186,Ellie Goulding; Juice WRLD - Hate Me (with Juice WRLD)
Ellie Goulding - Hate Me (with Juice WRLD).mp3
#EXTINF:194,American Authors - Best Day Of My Life
American Authors - Best Day Of My Life.mp3
#EXTINF:168,GAYLE - abcdefu
GAYLE - abcdefu.mp3
#EXTINF:199,WALK THE MOON - Shut Up and Dance
WALK THE MOON - Shut Up and Dance.mp3
#EXTINF:236,Martin Garrix; Dean Lewis - Used To Love (with Dean Lewis)
Martin Garrix - Used To Love (with Dean Lewis).mp3
"""
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("POST request sent successfully.")
        else:
            print("Failed to send POST request. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    send_post_request()

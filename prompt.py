import openai
from halo import Halo
import config

openai.api_key = config.OPENAI_API_KEY
spinner = Halo(text='Loading', spinner='dots')

def chat_gpt_completion(chat_message, append = False, usr_prompt = ""):


    spinner.start("text generating")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= chat_message
    )

    spinner.succeed("text generated")

    response = completion['choices'][0]["message"]["content"]

    if append:
        chat_message.append({"role": "assistant", "content": response})


    return response, chat_message


def response_to_dict(response):
        response_list = eval(response)
        result = {}

        for item in response_list:
            title, artist = item
            result[title] = artist

        return result

def generate_songs_from_books(books, message = []):
    if message != []:
        index = 0

        new_books_prompt = f"""
        Generate a 5 more songs inspired by the user's favorite books, which are: {books}
        Only return the list of songs according to the specification:
        [[Title1, Artist1], [Title2, Artist2], [Title3, Artist3], ...]

        For example:

        Favorite books: "Alice's Adventures in Wonderland"
        Response: [["White Rabbit", "Jefferson Airplane"], ["Down the Rabbit Hole", "Adam Lambert"], ["Painting Flowers", "All Time Low"], ["Cheshire Cat", "Blacklite District"], ["Mad Hatter", "Melanie Martinez"]]

        Now create a unique playlist for these books following the format:
            Favourite books: {books}
            Response:
        """

        while index < 3:
            message.append({"role": "user", "content": new_books_prompt})
            response, message = chat_gpt_completion(message, append=True)
            try:
                songDict = response_to_dict(response)
                break
            except:
                index += 1;
                print("Error in response_to_dict, Trying Again")

        if index >= 3:
            return Exception
    else:
        system_prompt = """
        You are a song recommender. The user will provide you with a list of their favorite books, and your task is to create a playlist of songs inspired by those books.
        Please return the song titles and the corresponding artists as a comma-separated list.
        """

        user_prompt = f"""
        You are a song recommender and will create playlists based on users' favorite books.
        Your task is to generate a playlist according to the user's favorite books and return the playlist in the specified format.
        If the book isn't found assume it's closest equivelent
        Generate at least 10 songs
        Only return the list of songs nothing else

        Specification:

            The generated playlist should be in this format: [[Title1, Artist1], [Title2, Artist2], [Title3, Artist3], ...]

        Examples:

            Favorite books: "Alice's Adventures in Wonderland"
            Response: [["White Rabbit", "Jefferson Airplane"], ["Down the Rabbit Hole", "Adam Lambert"], ["Painting Flowers", "All Time Low"], ["Cheshire Cat", "Blacklite District"], ["Mad Hatter", "Melanie Martinez"], ["Wonderland", "Taylor Swift"], ["Alice", "Avril Lavigne"], ["Living in a Dream", "Finger Eleven"], ["Go Ask Alice", "The Unlikely Candidates"], ["Curiouser", "Grace VanderWaal"]]

            Favorite books: "Dracula"
            Response: [["Love Song for a Vampire", "Annie Lennox"], ["Dracula's Wedding", "OutKast"], ["Bela Lugosi's Dead", "Bauhaus"], ["Vampire Heart", "HIM"], ["Nosferatu", "Blue Öyster Cult"], ["Fresh Blood", "Eels"], ["Bloodletting (The Vampire Song)", "Concrete Blonde"], ["Vampire", "Tribal Seeds"], ["Moon Over Goldsboro", "The Mountain Goats"], ["Dracula Teeth", "The Last Shadow Puppets"]]

            Favorite books: "One Hundred Years of Solitude"
            Response: [["Macondo", "Oscar Chávez"], ["Solitude", "Black Sabbath"], ["One Hundred Years", "The Cure"], ["Aureliano", "Bamboo"], ["García Márquez", "El Club de los Poetas Violentos"], ["Lonely Solitude", "Mike Zito"], ["Cien Años", "Pedro Infante"], ["Remedios", "Aterciopelados"], ["Amaranta", "Luis Eduardo Aute"], ["El Coronel", "Los Fabulosos Cadillacs"]]

            Favorite books: "The Picture of Dorian Gray"
            Response: [["Dorian", "Agnes Obel"], ["The Portrait", "Danny Elfman"], ["Dorian's Decay", "Cinema Bizarre"], ["The Picture", "Hubert Kah"], ["Age of Innocence", "Smashing Pumpkins"], ["Eternal Youth", "Rudimental"], ["Portrait of Dorian Gray", "The Scars"], ["Vanity", "Lady Gaga"], ["Forever Young", "Alphaville"], ["Youth", "Troye Sivan"]]

            Favorite books: "Slaughterhouse-Five"
            Response: [["Billy Pilgrim", "Kurt Vile"], ["Slaughterhouse", "Powerman 5000"], ["Dresden", "Orchestral Manoeuvres in the Dark"], ["So It Goes", "Nick Lowe"], ["Time Traveler", "A Skylit Drive"], ["Unstuck in Time", "Caspian"], ["Kilgore Trout", "Stoned Jesus"], ["Trafalmadorian", "The Mantras"], ["Five to One", "The Doors"], ["War Is Over", "Low Roar"]]

            Favorite books: "To Kill a Mockingbird, The Great Gatsby"
            Response: [["Mockingbird", "Eminem"], ["Young and Beautiful", "Lana Del Rey"], ["Darcy's Theme", "Dario Marianelli"], ["Testify", "Rage Against the Machine"], ["Harper", "Paul McDonald"], ["Jay Gatsby", "The Great Gatsby Orchestra"], ["Atticus", "The Noisettes"], ["A Little Party Never Killed Nobody", "Fergie"], ["Scout's Honor", "Blue Mitchell"], ["Gatsby's Theme", "Gotan Project"]]

            Favorite books: "Moby Dick, Lord of the Flies, Brave New World"
            Response: [["Call Me Ishmael", "Mastodon"], ["Savages", "Marina"], ["Brave New World", "Iron Maiden"], ["Pigs (Three Different Ones)", "Pink Floyd"], ["Leviathan", "Mastodon"], ["Beast", "Nico Vega"], ["Soma", "Deadmau5"], ["The Island", "Pendulum"], ["The Whale Song", "Modest Mouse"], ["The Lord of the Flies", "Carnivore"]]

            Favorite books: "The Hobbit, Fahrenheit 451, Catch-22, and Frankenstein"
            Response: [["Misty Mountains", "Richard Armitage"], ["Burning Books", "Hans Zimmer"], ["Catch-22", "You Me At Six"], ["Monster", "Paramore"], ["Song of the Lonely Mountain", "Neil Finn"], ["The Fireman", "Joe Hill"], ["22 (Over Soon)", "Bon Iver"], ["It's Alive", "A Perfect Circle"], ["Far Over the Misty Mountains Cold", "Howard Shore"], ["Fahrenheit 451", "Tangerine Dream"]]

            Favorite books: "The Catcher in the Rye, Crime and Punishment, Heart of Darkness, and The Odyssey"
            Response: [["Holden", "Santigold"], ["Punishment", "Biohazard"], ["Heart of Darkness", "Arch Enemy"], ["Sirens", "Pearl Jam"], ["Catcher in the Rye", "Guns N' Roses"], ["Raskolnikov", "Ezra Furman"], ["Into the Darkness", "Avantasia"], ["Calypso", "John Denver"], ["Caulfield", "The Retuses"], ["Crime & Punishment", "Fyfe Dangerfield"]]


        Now create a unique playlist for these books following the format:
            Favourite books: {books}
            Response:
        """

        index = 0
        while index < 3:
            message = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

            response, message = chat_gpt_completion(message, append=True)

            try:
                songDict = response_to_dict(response)
                break
            except:
                index += 1;
                print("Error in response_to_dict, Trying Again")

        if index >= 3:
            return Exception

    return songDict, message

def generate_songs_from_movies(movies, message=[]):
    if message != []:
        index = 0

        new_movies_prompt = f"""
        Generate 5 more songs inspired by the user's favorite movies, which are: {movies}
        Only return the list of songs according to the specification:
        [[Title1, Artist1], [Title2, Artist2], [Title3, Artist3], ...]

        For example:

        Favorite movies: "The Matrix"
        Response: [["Clubbed to Death", "Rob Dougan"], ["Wake Up", "Rage Against the Machine"], ["Spybreak!", "Propellerheads"], ["My Own Summer", "Deftones"], ["Dragula", "Rob Zombie"]]

        Now create a unique playlist for these movies following the format:
            Favorite movies: {movies}
            Response:
        """

        while index < 3:
            message.append({"role": "user", "content": new_movies_prompt})
            response, message = chat_gpt_completion(message, append=True)

            try:
                songDict = response_to_dict(response)
                break
            except:
                index += 1;
                print("Error in response_to_dict, Trying Again")

        if index >= 3:
            return Exception
    else:
        system_prompt = """
        You are a song recommender. The user will provide you with a list of their favorite movies, and your task is to create a playlist of songs inspired by those movies.
        Please return the song titles and the corresponding artists as a comma-separated list.
        """

        user_prompt = f"""
        You are a song recommender and will create playlists based on users' favorite movies.
        Your task is to generate a playlist according to the user's favorite movies and return the playlist in the specified format.
        Only return the list of songs nothing else
        If the movie isn't found, assume its closest equivalent.
        Generate at least 10 songs.


        Specification:
            The generated playlist should be in this format: [[Title1, Artist1], [Title2, Artist2], [Title3, Artist3], ...]

        Examples:

            Favorite movies: "The Matrix"
            Response: [["Clubbed to Death", "Rob Dougan"], ["Wake Up", "Rage Against the Machine"], ["Spybreak!", "Propellerheads"], ["My Own Summer", "Deftones"], ["Dragula", "Rob Zombie"], ["Bad Blood", "Ministry"], ["Prime Audio Soup", "Meat Beat Manifesto"], ["Mona Lisa Overdrive", "Juno Reactor"], ["Mindfields", "The Prodigy"], ["Dissolved Girl", "Massive Attack"]]

            Favorite movies: "Inception"
            Response: [["Time", "Hans Zimmer"], ["Dream Is Collapsing", "Hans Zimmer"], ["Mombasa", "Hans Zimmer"], ["One Simple Idea", "Hans Zimmer"], ["528491", "Hans Zimmer"], ["Inception (Junkie XL Remix)", "Hans Zimmer"], ["Old Souls", "Hans Zimmer"], ["Waiting for a Train", "Hans Zimmer"], ["Paradox", "Hans Zimmer"], ["We Built Our Own World", "Hans Zimmer"]]

            Favorite movies: "The Lord of the Rings"
            Response: [["Concerning Hobbits", "Howard Shore"], ["May It Be", "Enya"], ["The Breaking of the Fellowship", "Howard Shore"], ["Gollum's Song", "Emilíana Torrini"], ["Into the West", "Annie Lennox"], ["The Riders of Rohan", "Howard Shore"], ["The Bridge of Khazad-dûm", "Howard Shore"], ["The White Tree", "Howard Shore"], ["The Ring Goes South", "Howard Shore"], ["Amon Hen", "Howard Shore"]]

            Favorite movies: "Blade Runner"
            Response: [["Main Titles", "Vangelis"], ["Blush Response", "Vangelis"], ["Wait for Me", "Vangelis"], ["Rachel's Song", "Vangelis"], ["Love Theme", "Vangelis"], ["One More Kiss, Dear", "Don Percival & Vangelis"], ["Blade Runner Blues", "Vangelis"], ["Memories of Green", "Vangelis"], ["Tears in Rain", "Vangelis"], ["End Titles", "Vangelis"]]

            Favorite movies: "Pulp Fiction"
            Response: [["Misirlou", "Dick Dale & His Del-Tones"], ["Son of a Preacher Man", "Dusty Springfield"], ["Jungle Boogie", "Kool & The Gang"], ["Bustin' Surfboards", "The Tornadoes"], ["Lonesome Town", "Ricky Nelson"], ["Bullwinkle Part II", "The Centurions"], ["Girl, You'll Be a Woman Soon", "Urge Overkill"], ["Surf Rider", "The Lively Ones"], ["Ezekiel 25:17", "Samuel L. Jackson"], ["You Never Can Tell", "Chuck Berry"]]

            Favorite movies: "The Shawshank Redemption"
            Response: [["May", "Thomas Newman"], ["Brooks Was Here", "Thomas Newman"], ["Zihuatanejo", "Thomas Newman"], ["So Was Red", "Thomas Newman"], ["End Title", "Thomas Newman"], ["Sisters", "Thomas Newman"], ["Mozart: The Marriage of Figaro", "Wolfgang Amadeus Mozart"], ["Duettino: Sull'aria", "Kiri Te Kanawa & Edita Gruberova"], ["Shawshank Prison (Stoic Theme)", "Thomas Newman"], ["New Fish", "Thomas Newman"]]

            Favorite movies: "In the Mood for Love, Chungking Express"
            Response: [["Yumeji's Theme", "Shigeru Umebayashi"], ["Baroque", "Michael Galasso"], ["ITMFL", "Danny Chung"], ["California Dreamin'", "The Mamas & The Papas"], ["Dreams", "Faye Wong"], ["Chungking Express Theme", "Fung Hang Record Ltd."], ["What a Hero", "Jackie Chan"], ["Police Story Theme", "Jackie Chan"], ["A Taste of Kung Fu", "Michael Lai"], ["Super Cop", "Tommy Wai"]]

            Favorite movies: "The Godfather, Goodfellas, Scarface"
            Response: [["Speak Softly Love", "Andy Williams"], ["Rags to Riches", "Tony Bennett"], ["Gimme Shelter", "The Rolling Stones"], ["Tony's Theme", "Giorgio Moroder"], ["Love Theme From The Godfather", "Nino Rota"], ["Layla (Piano Exit)", "Derek and the Dominos"], ["Push It to the Limit", "Paul Engemann"], ["The Godfather Waltz", "Nino Rota"], ["Life Is But a Dream", "The Harptones"], ["She's On Fire", "Amy Holland"]]

            Favorite movies: "Fight Club, The Dark Knight, Inception"
            Response: [["Where Is My Mind?", "Pixies"], ["The Dark Knight Theme", "Hans Zimmer"], ["Time", "Hans Zimmer"], ["The Dust Brothers", "Corporate World"], ["Molossus", "Hans Zimmer & James Newton Howard"], ["Dream Is Collapsing", "Hans Zimmer"], ["This Is Your Life", "The Dust Brothers"], ["A Watchful Guardian", "Hans Zimmer & James Newton Howard"], ["Mombasa", "Hans Zimmer"], ["Stealing Fat", "The Dust Brothers"]]

            Favorite movies: "Eternal Sunshine of the Spotless Mind, The Truman Show, Being John Malkovich"
            Response: [["Everybody's Gotta Learn Sometime", "Beck"], ["Truman Sleeps", "Philip Glass"], ["Malkovich Malkovich", "Carter Burwell"], ["Waking Up", "Jon Brion"], ["Dreaming of Fiji", "Philip Glass"], ["Puppet Love", "Carter Burwell"], ["Phone Call", "Jon Brion"], ["Anthem Part 2", "Philip Glass"], ["Craig Plots", "Carter Burwell"], ["Row", "Jon Brion"]]

        Now create a unique playlist for these movies following the format:
            Favorite movies: {movies}
            Response:
        """

        index = 0
        while index < 3:
            message = [{"role": "system", "content": system_prompt},
                       {"role": "user", "content": user_prompt}]
            response, message = chat_gpt_completion(message, append=True)
            try:
                songDict = response_to_dict(response)
                break
            except:
                index += 1;
                print("Error in response_to_dict, Trying Again")

        if index >= 3:
            return Exception

    return songDict, message

def generate_songs_from_games(games, message=[]):
    if message != []:
        index = 0

        new_games_prompt = f"""
        Generate 5 more songs inspired by the user's favorite games, which are: {games}
        Only return the list of songs according to the specification:
        [[Title1, Artist1], [Title2, Artist2], [Title3, Artist3], ...]

        For example:

        Favorite games: "The Legend of Zelda: Ocarina of Time"
        Response: [["Title Theme", "Koji Kondo"], ["Hyrule Field Main Theme", "Koji Kondo"], ["Gerudo Valley", "Koji Kondo"], ["Song of Storms", "Koji Kondo"], ["Zelda's Lullaby", "Koji Kondo"]]

        Now create a unique playlist for these games following the format:
            Favorite games: {games}
            Response:
        """

        while index < 3:
            message.append({"role": "user", "content": new_games_prompt})
            response, message = chat_gpt_completion(message, append=True)

            try:
                songDict = response_to_dict(response)
                break
            except:
                index += 1;
                print("Error in response_to_dict, Trying Again")

        if index >= 3:
            return Exception
    else:
        system_prompt = """
        You are a song recommender. The user will provide you with a list of their favorite video games, and your task is to create a playlist of songs inspired by those games.
        Please return the song titles and the corresponding artists as a comma-separated list.
        """

        user_prompt = f"""
        You are a song recommender and will create playlists based on users' favorite video games.
        Your task is to generate a playlist according to the user's favorite games and return the playlist in the specified format.
        Only return the list of songs nothing else
        If the game isn't found, assume its closest equivalent.
        Generate at least 10 songs.


        Specification:
            The generated playlist should be in this format: [[Title1, Artist1], [Title2, Artist2], [Title3, Artist3], ...]

        Examples:

            Favorite games: "The Legend of Zelda: Ocarina of Time"
            Response: [["Title Theme", "Koji Kondo"], ["Hyrule Field Main Theme", "Koji Kondo"], ["Gerudo Valley", "Koji Kondo"], ["Song of Storms", "Koji Kondo"], ["Zelda's Lullaby", "Koji Kondo"], ["Kakariko Village", "Koji Kondo"], ["Lost Woods", "Koji Kondo"], ["Great Fairy Fountain", "Koji Kondo"], ["Ganondorf Battle", "Koji Kondo"], ["Majora's Mask", "Koji Kondo"]]

            Favorite games: "Final Fantasy VII"
            Response: [["Prelude", "Nobuo Uematsu"], ["Main Theme of Final Fantasy VII", "Nobuo Uematsu"], ["Tifa's Theme", "Nobuo Uematsu"], ["Aerith's Theme", "Nobuo Uematsu"], ["One-Winged Angel", "Nobuo Uematsu"], ["Bombing Mission", "Nobuo Uematsu"], ["The Highwind Takes to the Skies", "Nobuo Uematsu"], ["Jenova", "Nobuo Uematsu"], ["Opening Theme- Bombing Mission", "Nobuo Uematsu"], ["Cosmo Canyon", "Nobuo Uematsu"]]

            Favorite games: "The Elder Scrolls V: Skyrim"
            Response: [["Dragonborn", "Jeremy Soule"], ["Ancient Stones", "Jeremy Soule"], ["The City Gates", "Jeremy Soule"], ["Silent Footsteps", "Jeremy Soule"], ["Beneath the Ice", "Jeremy Soule"], ["The White River", "Jeremy Soule"], ["Sky Above, Voice Within", "Jeremy Soule"], ["Death in the Darkness", "Jeremy Soule"], ["Shattered Shields", "Jeremy Soule"], ["Sovngarde", "Jeremy Soule"]]

            Favorite games: "Mass Effect 2"
            Response: [["Suicide Mission", "Jack Wall"], ["The Illusive Man", "Jack Wall"], ["The Normandy Reborn", "Jack Wall"], ["The Lazarus Project", "Jack Wall"], ["Thane", "Jack Wall"], ["The End Run", "Jack Wall"], ["The Collector Base", "Jack Wall"], ["The Human Reaper", "Jack Wall"], ["Tali", "Jack Wall"], ["Legion", "Jack Wall"]]

            Favorite games: "Red Dead Redemption 2, Halo: Combat Evolved"
            Response: [["That's the Way It Is", "Daniel Lanois"], ["Outlaws from the West", "Woody Jackson"], ["Cruel, Cruel World", "Willie Nelson"], ["Halo Theme", "Martin O'Donnell & Michael Salvatori"], ["Brothers in Arms", "Martin O'Donnell & Michael Salvatori"], ["The Last Spartan", "Martin O'Donnell & Michael Salvatori"], ["Rockstar", "Woody Jackson"], ["Unshaken", "D'Angelo"], ["Truth and Reconciliation Suite", "Martin O'Donnell & Michael Salvatori"], ["Enough Dead Heroes", "Martin O'Donnell & Michael Salvatori"]]

            Favorite games: "BioShock, Portal, Deus Ex: Human Revolution"
            Response: [["Welcome to Rapture", "Garry Schyman"], ["Cohen's Masterpiece", "Garry Schyman"], ["Dancers on a String", "Garry Schyman"], ["Still Alive", "Jonathan Coulton"], ["Want You Gone", "Jonathan Coulton"], ["Self Esteem Fund", "Kelly Bailey"], ["Icarus - Main Theme", "Michael McCann"], ["The Mole", "Michael McCann"], ["Detroit City Ambient Part 1", "Michael McCann"], ["And Away We Go", "Michael McCann"]]

            Favorite games: "The Last of Us, God of War (2018), Uncharted 4: A Thief's End"
            Response: [["The Last of Us (Main Theme)", "Gustavo Santaolalla"], ["The Quarantine Zone (20 Years Later)", "Gustavo Santaolalla"], ["All Gone (No Escape)", "Gustavo Santaolalla"], ["God of War", "Bear McCreary"], ["Memories of Mother", "Bear McCreary"], ["A Giant's Prayer", "Bear McCreary"], ["Nate's Theme 4.0", "Henry Jackman"], ["A Thief's End", "Henry Jackman"], ["Brother's Keeper", "Henry Jackman"], ["For Better or Worse", "Henry Jackman"]]

        Now create a unique playlist for these games following the format:
            Favorite games: {games}
            Response:
        """

        index = 0
        while index < 3:
            message = [{"role": "system", "content": system_prompt},                   {"role": "user", "content": user_prompt}]
            response, message = chat_gpt_completion(message, append=True)
            try:
                songDict = response_to_dict(response)
                break
            except:
                index += 1;
                print("Error in response_to_dict, Trying Again")

        if index >= 3:
            return Exception

    return songDict, message
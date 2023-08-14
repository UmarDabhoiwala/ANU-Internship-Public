recipePrompt = """
Help me write recipes in the Cooklang Specification: Below is an example of a recipe written in the specification, I have delimited the start and end of the recipe with @startRecipe and @endRecipe 

@startRecipe
>> source: https://www.dinneratthezoo.com/wprm_print/6796
>> total time: 6 minutes
>> servings: 2

Place the @apple juice{1,5%cups}, @banana{one sliced}, @frozen mixed berries{1,5%cups} and @vanilla greek yogurt{3/4%cup} in a #blender{}; blend until smooth. If the smoothie seems too thick, add a little more liquid (1/4 cup). 

Taste and add @honey{} if desired. Pour into two glasses and garnish with fresh berries and mint sprigs if desired.
@endRecipe

For further context, here is some more specific detail on the specification:

@startContext
Comments

You can add comments up to the end of the line to Cooklang text with --.

-- Don't burn the roux!

Mash @potato{2%kg} until smooth -- alternatively, boil 'em first, then mash 'em, then stick 'em in a stew.

Or block comments with [- comment text -].

Slowly add @milk{4%cup} [- TODO change units to litres -], keep mixing

Metadata

You can add metadata tags to your recipe for information such as source (or author), meal, total prep time, and number of people served.

>> source: https://www.gimmesomeoven.com/baked-potato/
>> time required: 1.5 hours
>> course: dinner

Cookware

You can define any necessary cookware with #. Like ingredients, you don’t need to use braces if it’s a single word.

Place the potatoes into a #pot.
Mash the potatoes with a #potato masher{}.

Timer

You can define a timer using ~.

Lay the potatoes on a #baking sheet{} and place into the #oven{}. Bake for ~{25%minutes}.

Timers can have a name too:

Boil @eggs{2} for ~eggs{3%minutes}.

@endContext

Now create your own recipe and give it back in this format, it can be anything you like just respond in the correct specification.
"""

recipePrompt2 = """
Help me write recipes in Markdown: Below is an example of a recipe written in the specification. Follow it exactly 

# Homemade Cinnamon Rolls

Made from scratch, these soft, creamy cinnamon rolls will leave you feeling happy and satisfied, even on the coldest winter nights. Pour over a generous, sugary glaze for the warm, comforting snack you know you deserve!

- categories: desserts, baking, feel good, comfort food
- yields: 18 cinnamon rolls
- servings: 9
- prep: 20 mins
- cook: 20 mins


## Ingredients

### Dough

- 2 cups all-purpose [flour]
- 2 tbsp [white sugar]
- 2 tsp [baking powder]
- 1 tsp [salt]
- 3 tbsp [butter], softened
- 3/4 cup [milk]
- 1 [egg]

### Filling

- 1/2 cup [white sugar]
- 1/2 cup [brown sugar]
- 1 tbsp [ground cinnamon]

### Cream Cheese Frosting

- 1 cup [powdered sugar]
- 4 oz [cream cheese], softened
- 1/4 cup [butter], softened
- 1/2 tsp [vanilla extract]

## Instructions

1. Preheat oven to 400 degrees. Brush a [9" baking dish] with 2 tbsp [butter].

2. Whisk [flour], 2 tbsp [white sugar], [baking powder], and [salt] together in a large bowl.

3. Work 3 tbsp softened [butter] into [flour] mixture using your hands. Beat [milk] and [egg] together in another bowl; pour into flour-butter mixture and stir with a spatula until a soft dough forms.

4. Whisk 1/2 cup [white sugar], [brown sugar], and [cinnamon] together in a small bowl. Sprinkle 1/2 of the cinnamon sugar mixture in the bottom of the prepared baking dish.

Sprinkle remaining cinnamon sugar over butter-brushed dough. Roll dough around filling to form a log; cut log into 18 rolls and place rolls in the prepared baking dish.

5. Bake in the preheated oven until rolls are set, 20 to 25 minutes.

6. Beat [powdered sugar], [cream cheese], 1/4 cup softened [butter], and [vanilla extract] together in a bowl until frosting is smooth. Top hot cinnamon rolls with cream cheese frosting.

## Notes
Don't need as much? Cut the recipe in half and bake for only 15 minutes!

Now create your own recipe and give it back in this format, it can be anything you like just respond in the correct specification.

"""

def getRecipePrompt(name, cuisine = False, protien = False, made_recipes = "", made_test = False):
    
    if made_test:
        if name == "":
            recipeArg = f"Now create a recipe for whatever you want but not related to these {made_recipes}"
        else: 
            if cuisine == True:
                recipeArg = f"Now create a recipe in the style of {name} cuisine but not related to these {made_recipes}"
            elif protien == True:
                recipeArg = f"Now create a recipe that has {name} but not related to these {made_recipes}"
            else: 
                recipeArg = f"Now create a recipe for {name}"
    else: 
        if name == "":
            recipeArg = f"Now create a recipe for whatever you want "
        else: 
            if cuisine == True:
                recipeArg = f"Now create a recipe in the style of {name} cuisine"
            elif protien == True:
                recipeArg = f"Now create a recipe that has {name}"
            else: 
                recipeArg = f"Now create a recipe for {name}"
              
    prompt = f"""
    Help me write recipes in Markdown: Below is an example of a recipe written in the specification. Follow it exactly 

    # Homemade Cinnamon Rolls

    Made from scratch, these soft, creamy cinnamon rolls will leave you feeling happy and satisfied, even on the coldest winter nights. Pour over a generous, sugary glaze for the warm, comforting snack you know you deserve!

    - categories: desserts, baking, feel good, comfort food
    - yields: 18 cinnamon rolls
    - servings: 9
    - prep: 20 mins
    - cook: 20 mins


    ## Ingredients

    ### Dough

    - 2 cups all-purpose [flour]
    - 2 tbsp [white sugar]
    - 2 tsp [baking powder]
    - 1 tsp [salt]
    - 3 tbsp [butter], softened
    - 3/4 cup [milk]
    - 1 [egg]

    ### Filling

    - 1/2 cup [white sugar]
    - 1/2 cup [brown sugar]
    - 1 tbsp [ground cinnamon]

    ### Cream Cheese Frosting

    - 1 cup [powdered sugar]
    - 4 oz [cream cheese], softened
    - 1/4 cup [butter], softened
    - 1/2 tsp [vanilla extract]

    ## Instructions

    1. Preheat oven to 400 degrees. Brush a [9" baking dish] with 2 tbsp [butter].

    2. Whisk [flour], 2 tbsp [white sugar], [baking powder], and [salt] together in a large bowl.

    3. Work 3 tbsp softened [butter] into [flour] mixture using your hands. Beat [milk] and [egg] together in another bowl; pour into flour-butter mixture and stir with a spatula until a soft dough forms.

    4. Whisk 1/2 cup [white sugar], [brown sugar], and [cinnamon] together in a small bowl. Sprinkle 1/2 of the cinnamon sugar mixture in the bottom of the prepared baking dish.

    Sprinkle remaining cinnamon sugar over butter-brushed dough. Roll dough around filling to form a log; cut log into 18 rolls and place rolls in the prepared baking dish.

    5. Bake in the preheated oven until rolls are set, 20 to 25 minutes.

    6. Beat [powdered sugar], [cream cheese], 1/4 cup softened [butter], and [vanilla extract] together in a bowl until frosting is smooth. Top hot cinnamon rolls with cream cheese frosting.

    ## Notes
    Don't need as much? Cut the recipe in half and bake for only 15 minutes!

    {recipeArg}, and give it back in this format.

    """    
    
    return prompt
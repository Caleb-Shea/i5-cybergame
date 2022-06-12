# i5-cybergame
A wargame simulation made by the i5 cyber element, with inspiration from the i5 intel element.

## Contributers:
- Michaela Kovalsky (Project Manager)
- Caleb Shea (Development Lead)
- ??? (Quality Analysis Tester)
- ??? (Graphic Designer)

### Menus:
- New window? Or just stick with the one screen?
- showing the purchased upgrades for each satellite on the main screen would be cool

#### Brainstorming:
- Acquitions will be where the player buys satellites
    - Each satellite will require personnel to keep running, the more people are assigned to a satellite, the higher level the satellite will be
- Ops will be where the player completes missions to increase reputation and ___
    - Spending money, time, and workers
- Intel will be where the player attends briefs to unlock missions and increase reputation
    - Briefs are unlocked by purchasing new satellites and completing missions
    - Cost very little money but require a certain number of free workers to attend
        - You can only attend briefs if you have an available worker?
- Cyber will be where the player counters threats to their missions and satellites
    - Can either be a huge part of the game, or a pretty small part of it
    - Offensive/ Defensive teams
- Personnel will be where the player hires contractors, workers, and other people
    - This is where the player can see what all their workers are doing
    - People (in the 1000s) will be shown what they're current task is
    - Bar graph?
- Research will be where the player unlocks the capabilities to buy new satellites, attend new briefs, and hire better workers

### Win conditions
- Beat Russia/China
    - Launch a pre-emptive strike by upgrading cyber or ops to a high enough level
    - Or, develop strong enough defenses that when the attack comes, it causes no harm
- Pure 'clicker game'
    - No end goal/lose condition
    - Just a fun mess around game

Leaning towards Russia/China situation

### Zoom animation ideas:
- Zoom in so far the node fills the screen, then zoom out to see everything
- Zoom in as normal, then have all child nodes fly out

### General:
- `pygame.sprite.LayeredUpdates()` is a thing. At some point this might be helpful
- Use elliptical orbits
- `pyg.Surface.fill()` is hardware accelerated. Maybe switch?
- Compile with [PyInstaller](https://pyinstaller.org/en/stable/)

### Todo list:
- Move node menus to the HUD class
- Restructure HUD rendering to limit functions
- Add scroll limits
- [FullMenu] Move logic from render_XXX() to update_XXX()
- Easter eggs :)

## Credits:
- https://freesound.org/people/EminYILDIRIM/sounds/536108/

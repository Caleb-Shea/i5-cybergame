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
- Acquitions will be where the player buys satellites and ___
- Ops will be where the player completes missions to increase reputation and ___
    - Spending money and time?
- Intel will be where the player attends briefs to unlock missions and increase reputation
    - Briefs are unlocked by purchasing new satellites and completing missions
    - Cost very little (free?), but have a 'cooldown' on them
        - You can only attend briefs if you have an available worker?
- Cyber will be where the player counters threats to their missions and satellites
    - Can either be a huge part of the game, or a pretty small part of it
- Personnel will be where the player hires contractors, workers, and other people
    - This is where the player can see what all their workers are doing?
    - Small number of people or very large numbers?
- Research will be where the player unlocks the capabilities to buy new satellites, attend new briefs, and hire better workers
- Are all tabs available off the bat? Or will they be spaced out?
- If the end goal is still becoming a 4*, how does that happen, and what rank will you start at?
- Will the events/missions/satellites/basically everything be hand-crafted, or will it be psuedorandom?

### Zoom animation ideas:
- Zoom in so far the node fills the screen, then zoom out to see everything
- Zoom in as normal, then have all child nodes fly out

### General:
- There is a layered group built-in to pygame. That might be useful at some point
- Use elliptical orbits
- `pyg.Surface.fill()` is hardware accelerated. Maybe switch?
- Compile with [PyInstaller](https://pyinstaller.org/en/stable/)

### Todo list:
- Move node menus to the HUD class

## Credits:
- https://freesound.org/people/EminYILDIRIM/sounds/536108/

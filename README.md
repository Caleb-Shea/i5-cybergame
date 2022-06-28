# i5-cybergame
A wargame simulation made by the i5 cyber element, with inspiration from the i5 intel element.

## Contributers:
- Michaela Kovalsky (Project Manager)
- Caleb Shea (Development Lead)
- ??? (Quality Analysis Tester)
- ??? (Graphic Designer)
- ??? (Content Creator)
- ??? (Story Planner)

### Brainstorming:
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
    - People (in the 1000s?) will be shown what they're current task is
    - Bar graph?
- Events will be where the player interacts with the news events they saw on the news ticker
    - The player should not spend extensive time on this menu

### Win conditions
- Beat Russia/China
    - Launch a pre-emptive strike by upgrading cyber and/or ops to a high enough level
    - Or, develop strong enough defenses that when the attack comes, it causes no harm

### General:
- `pygame.sprite.LayeredUpdates()` is a thing. At some point this might be helpful
- `pyg.Surface.fill()` is hardware accelerated. Maybe switch?
- Compile with [PyInstaller](https://pyinstaller.org/en/stable/) or [Nuitka](https://nuitka.net/doc/user-manual.html)

### Materials needed:
|Content|Approx Quantity|
|-----|-----|
|Newsreels|Like 100+ ideally|
|Operation names|~30*|
|Intel brief names|~20*|
|Satellite names w/ description, stats, and pictures|5-6|
|Missile names w/ description, stats, and pictures|3-4|
|Pictures w/ animation for Earth|1-2|
|Pictures w/ animation for satellites/missiles|9|
|UI/UX|1-3 styles|
|A soundtrack|3+ ~3-4 min tracks|

*Could be pseudorandomly generated

### Todo list:
- __HUD:__ Restructure HUD rendering to limit number of functions
- __Acquisitions:__ Add stats panel underneath the picture
- Change Acquitions/Cyber tab to use surfaces
- Only render objects that are on screen
- __EMenu:__ Move earth to the left when closing earth vignette
- __EMenu:__ Add scroll limits to main screen?
- __FullMenu:__ Add ability for newline characters in acquisitions tab descriptions
- Figure out what to do with the satellite nodes system
    - __HUD:__ Move node menus to the HUD class
- Add interactivity e.g. minigames and/or/like an actual game game
- __Intel:__ Literally redo everything
- Round/square-off corners of rects
- Easter eggs/Achievements

### Known bugs:
- __Acquisitions:__ Double click buys it three+ times on a trackpad
- __FullMenu:__ On bigger screens, the border is offset
- Pressing a key will sometimes stop the next mouse click from being registered
- Sometimes, the earth will render on the topleft of the screen

## Credits:
- https://freesound.org/people/EminYILDIRIM/sounds/536108/
- https://freemusicarchive.org/music/nul-tiel-records/electronica/empty-head-1/
- https://loading.io

# i5-cybergame
A wargame simulation made by the i5 cyber element, with inspiration from the i5 intel element.

## Contributers:
- Michaela Kovalsky (Project Manager)
- Caleb Shea (Development Lead)
- Casey Landrum (Content, QA)
- ??? (Quality Analysis Tester)
- ??? (Graphic Designer)
- ??? (Content Creator)
- ??? (Story Planner)

### Brainstorming:
- Cutscenes?
  - After buying a new sat, attending a brief, etc., should there be a 1-3 second cutscene highlighting the new thing?
- Background animations behind each fullmenu graphics
- Ops gameplay:
  - Grid based movement or free move?
  - Do the ground forces exist?
    - If so:
      - Do we control them?
        - If we control them, how do the satellites play into that?
        - If we don't (i.e. AI does), how should we render them so they aren't obtrusive?
      - If the ground forces exist, we have more options for individual mission objectives, but the gameplay could be messier/higher learning curve
        - Is that ok?
    - If not:
      - What is the goal of a mission?
      - What do we render other than the satellites themselves?
        - Earth or space background?
      - How do we keep managing just satellites engaging?
  - What do we include other than satellites?
    - See above for ground forces discussion
    - Cities?
  - One main enemy or several?
    - One is easier from a game comprehension standpoint
    - Several is more realistic
    - If we add several, things will get complicated quickly
      - Is that ok?
  - Will missions be static?
    - I.e., will the main story be the same every time
  - How do you win?
    - Eliminate enemy forces?
    - Guide friendlies to a target?
    - Rescue passive forces?
  - What happens when you lose?
    - Should you just have replay the mission?
      - Lower stakes, and the story will be static/less dynamic
      - Easier
    - Should the mission just be lost and you must move on?
      - Higher stakes, and will allow for a dynamic story
      - Requires more planning on the part of the player
        - More engagement
  - Should it be a hard game or an easy one?

### Win conditions
- Beat Russia/China
  - Launch a pre-emptive strike by upgrading cyber and/or ops to a high enough level
  - Or, develop strong enough defenses that when the attack comes, it causes no harm

### General:
- `pygame.sprite.LayeredUpdates()` is a thing. At some point this might be helpful
- `pyg.Surface.fill()` is hardware accelerated. Maybe switch?
- Compile with [PyInstaller](https://pyinstaller.org/en/stable/)
  - `pyinstaller --add-data "assets;assets" --add-data "ticker_events.csv;." --add-data "ops_data.csv;." main.py`

### Name ideas/brainstorming:
- Astra
  - Astradiem
- Adamo
  - In latin, means to fall in love with
- Auora Borealis
- Invictus
  - Invictra
- Something with space
- Portmanteaus
- Easy to say
- Probably just one word
- If we want a website for it, use [pureWhoIs](https://purewhois.com)
- Cosmos
- i5?
- USAFA?
- Military at all?

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
|A soundtrack|3+ ~1-4 min tracks|
|Fonts|Title, Header, Sub-Header, and Body fonts|

*Could be pseudorandomly generated

### Todo list:
- __FullMenu:__ FIX INTEL TAB
- __EMenu:__ Move earth to the left when closing earth vignette
- __FullMenu:__ Add ability for newline characters in acquisitions tab descriptions
- Change Acquitions/Cyber tab to use surfaces
- __FullMenu:__ Standardize colors for each tab across the game
- __assets.py:__ Support dynamic loading of resources only when needed
- __FullMenu:__ Add support for larger displays (use percentages rather than absolutes)
- __assets.py:__ Restructure colors
- __FullMenu:__ Remove relative coords; replace with absolute
- __FullMenu:__ Decompose into smaller classes?
- Add ability to click on ticker to open events menu
- Easter eggs/Achievements

### Known bugs:
- Pressing a key will sometimes stop the next mouse click from being registered
- The EQ in the pause menu doesn't actually work lol
- If the screen size changes (e.g. the game is moved to a monitor), the game doesn't adjust

## Credits:
- https://freesound.org/people/EminYILDIRIM/sounds/536108/
- https://freesound.org/people/plasterbrain/sounds/423166/
- https://freemusicarchive.org/music/nul-tiel-records/electronica/empty-head-1/
- https://loading.io
- https://www.markdownguide.org/extended-syntax/#fenced-code-blocks
- https://inkarnate.com/
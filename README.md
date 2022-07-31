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
  - After buying a new sat, attending a brief, etc., should there be a 2-5 second cutscene highlighting the new thing?

- Ops gameplay:
  - On selection of mission location, one of the following happens:
    - XCOM style, except instead of people with guns, it's satellites with lasers and comms and shit. There is (unseen) ground/air troops that we are trying to enable to complete a mission.
    - XCOM style, except instead of people with guns, it's satellites with lasers and comms and shit. We can see the ground/air forces under us, they move on their own and we have to feed them info and destry enemies to allow them to make it to the goal. As the game goes on, the space force gets requested for more and more high profile cases that require more and more resources.
  - *Turn-based strategy fits the theme more, but real time action is arguably more enjoyable for a wider audience.

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
|A soundtrack|3+ ~1-4 min tracks|
|Fonts|Title, Header, Sub-Header, and Body fonts|

*Could be pseudorandomly generated

### Todo list:
- Add interactivity e.g. minigames and/or/like an actual game game
- __EMenu:__ Move earth to the left when closing earth vignette
- __FullMenu:__ Add ability for newline characters in acquisitions tab descriptions
- Change Acquitions/Cyber tab to use surfaces
- __FullMenu:__ Add support for larger displays (use percentages rather than absolutes)
- Round/square-off corners of rects
- Only render objects that are on screen
- Add ability to click on ticker to open events menu
- Easter eggs/Achievements

### Known bugs:
- Pressing a key will sometimes stop the next mouse click from being registered

## Credits:
- https://freesound.org/people/EminYILDIRIM/sounds/536108/
- https://freesound.org/people/plasterbrain/sounds/423166/
- https://freemusicarchive.org/music/nul-tiel-records/electronica/empty-head-1/
- https://loading.io
- https://www.markdownguide.org/extended-syntax/#fenced-code-blocks

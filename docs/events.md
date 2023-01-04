# Messages

What sort of messages are there?

Messages triggered by user input events.

User Inputs:
 - Pressing buttons
 - Pressing keys
 - Entering values

These user  each represent some sort request (press play, set speed etc.)

This would make sense to describe as 3 parts:
 - trigger (what event triggered the message, keystroke etc.)
 - payload (Message contents)
 - metadata (dictionary, including things like time sent)

What else might there be?

View updates:
 - player sends trackname to view
 - youtube rip complete updates view

These also have a trigger.

Lets try and piece together what these could look like.

Message:
- trigger: Trigger
    - ViewTrigger: button/key/set-value
    - ModelTrigger: value-update
- payload: Payload (different types)
    - SetValue
    - Press
    - Release
- metadata








Message:
 - Sender
 - Content
 - Type (Enum), relates to Content
 - Metadata (dict)

Sender:
 - Source - View/Model
 - Component - LeftDeck
 - Trigger - KeyPress/KeyRelease

Content Types:
 - Key
 - Button
 - ValueButton
 - SetValue

Key:
 - press_release
 - sym

Button:
 - press_release
 - element

ValueButton:
 - press_release
 - element
 - value

SetValue:
 - element
 - value
# HW6 Part 2: Chapter 10, Architectural Design

## Problem 10.1

**Using the architecture of a house as a metaphor, compare it with software architecture. How are they similar, and how are they different?**

A house and a software system both need a plan before anyone starts building. Here is how the parts line up:

- The **blueprint** of a house is like the **architecture diagram** of a program.
- **Rooms** are like **modules**. Each one has its own job, like a kitchen for cooking or a login module for signing in.
- **Doors and hallways** are like **interfaces and APIs**. They connect the rooms so people (or data) can move between them.
- The **foundation** is like the **database, operating system and framework**. Everything else sits on top of it.
- **Plumbing and wiring** run through the whole house, just like **logging and security** run through the whole program.
- **Building codes** are like **software standards and laws**, such as security rules or privacy laws.

**How they are similar:**
1. Both start by finding out what the owner or user needs.
2. Both make the big decisions first and the small details later.
3. In both, big changes made late are expensive. Moving a main wall is hard, and so is changing the database after the app is built.
4. Both care about quality, not just function. A house must be safe; software must be secure and reliable.
5. Both reuse known styles instead of inventing everything from scratch.

**How they are different:**
1. A house is physical and follows the laws of physics. Software is not physical, so its limits are complexity and cost.
2. Houses rarely change. Software changes all the time, so it must be designed to be easy to change.
3. Building a second house costs as much as the first. Copying software costs almost nothing.
4. Construction has very old, strict building codes and inspections. Software engineering is much younger and its rules are less strict.
5. You can see cracks in a wall, but problems in software design are hidden and can grow quietly.
6. Software can be built and released in small pieces. A house usually can't be lived in until most of it is done.

---

## Problem 10.3

**Some architectural styles are hierarchical and some are not. List each type. How are the non-hierarchical styles built?**

**Hierarchical styles** (one part controls the parts below it, like a tree):
- **Main program and subprograms:** the main program calls functions, which call smaller functions.
- **Remote procedure call:** the same idea, but the functions run on different computers.
- **Layered:** each layer only talks to the layer below it, like UI → business logic → database.

**Non-hierarchical styles** (the parts are equals; nobody is "the boss"):
- **Data-centered:** many programs share one central database.
- **Data-flow (pipe and filter):** data passes through a chain of steps, one after another.
- **Object-oriented:** objects send messages to each other as equals.

**How the non-hierarchical styles are built:**
- **Data-centered:** you set up one shared database. Every program reads and writes to it on its own. The database can also tell programs when something changes. Git is a good example.
- **Data-flow:** each step is its own small program that takes input and gives output. The steps are joined by pipes or queues. Each step doesn't need to know about the others. The Unix command `cat file | grep error | sort` is an example.
- **Object-oriented / message-based:** objects or services send messages to each other directly or through a message queue. Each one decides what to do when it gets a message. Chat apps and event-driven systems work this way.

---

## Problem 10.5

**Pick an application you know. Answer the control and data questions from Section 10.3.3.**

**Application: Spotify**

Spotify has an app on your phone or computer. The app talks to Spotify's servers, which are split into many small services (login, search, playlists, recommendations, payments). The music files themselves come from a content delivery network (CDN), which is a set of servers placed close to users.

### Control questions

**How is control managed?**
Control starts with the user. When you tap play or search, the app sends a request. A front server (the API gateway) passes the request to the right service, and that service handles it.

**Is there a control hierarchy?**
Inside the app, yes: the screen calls the logic, and the logic calls the network code. On the server side, not really. The services are mostly equal and each handles its own job.

**How do components pass control?**
In two ways. For things you wait for, like search results, the app calls the server and waits for an answer. For things that happen in the background, like recording which song you played, services send messages (events) to each other.

**How is control shared?**
Each service owns one job, such as playlists or payments. They work together by sending events, not by one service bossing the others around.

**What does the control layout look like?**
Requests from the app go through the gateway to the services, like spokes going out from a hub. Between services, it is more like a web, since they send events to each other.

**Is control synchronous or asynchronous?**
Both. Logging in, searching and starting a song are synchronous because you are waiting. Recommendations, downloads and play history are asynchronous and happen in the background.

### Data questions

**How is data passed between components?**
The app and servers send data as JSON over HTTPS. Services send events through a message system (Kafka). Music is streamed in small chunks from the CDN.

**Is the data flow continuous or occasional?**
Music is continuous: it keeps streaming while you listen. Everything else (playlists, likes, search) is sent only when needed.

**Is data passed around or shared globally?**
It is mostly passed from one part to another. Each service keeps its own database, and other services can't read it directly.

**Are there data components, and what do they do?**
Yes. Each service has its own database (for example, users or playlists). The CDN stores the music files. The phone keeps a local cache so you can listen offline. The event system keeps a log of what users do.

**How do the other parts use the data components?**
A service only reads and writes its own database. If another service needs that data, it has to ask through the service's API or listen to its events.

**Are data components passive or active?**
The databases and CDN are passive: they just answer requests. The event system is active: it pushes new events out to the services that care about them.

**How do data and control work together?**
Your actions start data requests. Changes in data, like "this song was played", send events that make other services act, such as updating your history or recommendations. While music plays, the amount of buffered music decides when the next chunk is downloaded.

---

## Problem 10.9

**Pick a mobile app you know. Judge it on economy, visibility, spacing, symmetry and emergence.**

**Application: WhatsApp**

**Economy (is it simple, with nothing extra?)**
Mostly yes. WhatsApp focuses on one thing: sending messages. It has only a few main parts: the phone app, the chat servers, storage for photos and videos, and push notifications. It is well known for serving billions of users with a small team. Newer features like Channels and Communities make it a little more cluttered.

**Visibility (are the design decisions easy to understand?)**
The main decisions are clear and public. Messages are end-to-end encrypted, your phone number is your account, and the server deletes messages once they are delivered. WhatsApp has published a paper explaining its encryption. The inside of its servers is private, so outsiders can't see everything.

**Spacing (are different jobs kept separate?)**
Yes. Encryption happens only on your phone. The server only passes along encrypted messages it can't read. Photos and videos are stored separately. Notifications go through Apple's and Google's services. One weak spot used to be that WhatsApp Web needed your phone to be online, but this was fixed with multi-device support.

**Symmetry (is it consistent and balanced?)**
Very much. Every user's app is equal; there's no special sender or receiver. One-to-one chats and group chats use the same system. The iPhone and Android apps work the same way. Business accounts and channels follow slightly different rules, which breaks the symmetry a little.

**Emergence (do useful features come from simple parts working together?)**
Yes. Read receipts (the grey and blue ticks), "typing…" and "online" all come from small, simple messages sent between phones through the server. No central controller manages them.

**Overall:** WhatsApp's architecture is simple, consistent and easy to scale. Its main risk is adding too many new features, which could make it more complicated. Those features should be kept as separate parts.

---

## Problem 10.2

**Give two or three example applications for each architectural style in Section 10.3.1.**

**Data-centered** (many programs share one central store of data)
1. Git: every command works on the same repository.
2. A bank or hospital system, where many apps read and update one shared database.
3. An IDE like VS Code, where the editor, debugger and search all share the same project information.

**Data-flow / pipe and filter** (data passes through a chain of steps)
1. A compiler: reading the code → checking it → optimizing it → producing machine code.
2. Unix commands joined with pipes, like `cat log | grep ERROR | sort`.
3. Video processing or data pipelines, where files go through several processing steps.

**Call and return** (a main program calls functions, locally or on another machine)
1. Simple command-line programs, like the stock quote program from Part 1 (`main` calls `get_quote`).
2. A payroll program with a main routine that calls modules for tax, pay and reports.
3. A mobile app calling a payment server using remote calls (RPC).

**Object-oriented** (objects with their own data talk to each other)
1. Desktop and Android apps, where buttons, windows and lists are objects.
2. Video games, where players, enemies and items are objects.
3. Simulation and drawing programs, where every shape is an object.

**Layered** (each layer uses only the layer below)
1. The internet's network stack: application → transport → network → link.
2. An operating system: apps → system calls → kernel → drivers → hardware.
3. A three-tier web app: web page → business logic → database.

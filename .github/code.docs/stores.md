# Stores

Stores load all the database data into memory when Swing Music is booted.

![Image: What happens when Swing Music is booted](../images/docs/stores-on-boot.png)

This is done for a few reasons:

1. To make things fast and snappy
2. Inference and post processing

## Making things fast

Prior to the Swing Music project, I went through quite a lot of music players. One of the reasons I despised them all, is how often they would freeze when I opened a huge Music folder of Music or searched for something in my library of 40, 000 music files. The ones that didn't freeze often had a very huge delay before giving me what I requested.

This is the main reason that stores are at the core of how Swing Music works. The main goal was to make all read operations have a time complexity of `~O(1)`. ie. all requests should feel like they take a constant time which should be near 1ms. We all know that's impossible, but 13ms is not that bad either for a library of 25, 000 songs. Right?

## Inference and post processing

You might have noticed that Swing Music tries to extract album version info from an album. Something like this:

![Inference in Swing Music](../images/docs/inference.png)

Other inferences and post processing activities that Swing Music does include:

- Removing remaster info from tracks
- Removing producers from track titles
- Extracting featured artists from track titles, etc.

All these activities are done when tracks are loaded into memory, when you start the app. Inferences and post processing helps standardize things and make things clean and relatable.

For example: If you have 3 versions of the Fleetwood Mac album `Rumours` like me, going to that album page will show you the other two at the bottom of the track list.

> [!TIP]
> Psst! You can disable the above behaviors anytime from the settings page.

## What about memory usage?

You might be thinking that storing thousands of items in memory would lead to high memory usage ... and you are right. But the thing is, if you have memory, why not use it to make your life snapier?

## The disadvantage

One of the disadvantages of using memory stores is that the app can't behave like a typical web server. That is, you can't use a WSGI server to run multiple instances if you need them. I couldn't even get gunicorn to run in the same thread as the stores (cries in C major), but that's not the problem here.

I don't know how many people share their entire music collection with thousands of users out there on the internet, because that's the only time you'd require that kind of setup. Starting from `v1.4.8`, Swing Music should be able to handle 10 users sending a crazy amount of requests to the server all at once (60r/s).

Now, a fix to this wsgi server situation (I think), would to move to [Shared Memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html). That way, you can load all the tracks into a shared memory location and multiple instances can read it and write to it, if needed.

I haven't tried out anything yet, so it's all hypothetical. I haven't met anyone who needs this kind of setup so it might not happen. Plus it's a lot of work.

## The stores

There are 3 stores:

1. Track store - `app/store/tracks.py`
2. Album store - `app/store/albums.py`
3. Artist store - `app/store/artists.py`

You can guess what kind of data each store holds. Each store has **class methods** which manipulate or retrieve data from it. Stores are uses as classes and thus not instantiated.

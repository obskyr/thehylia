# thehylia.py

`thehylia.py` is a [Python](https://www.python.org/) interface for getting [The Hylia](http://anime.thehylia.com/soundtracks/) soundtracks. It makes thehylia mass downloads a breeze. It's easy to use - check it!

From the command line:

```cmd
thehylia.py yakitate-japan-original-soundtrack
```

As an import:

```python
import thehylia
thehylia.download('yakitate-japan-original-soundtrack')
# And bam, you've got the Yakitate!! Japan soundtrack!
```

For video game music, [check out `khinsider.py`](https://github.com/obskyr/khinsider).

Carefully put together by [@obskyr](http://twitter.com/obskyr)!

### **[Download it here!](https://github.com/obskyr/thehylia/archive/master.zip)**

## Usage

Just run `thehylia.py` from the command line with the sole parameter being the soundtrack you want to download. Easy!

If you want, you can also add another parameter as the output folder, but that's optional.

You can also download FLAC versions of soundtracks (if available) as following:

```cmd
khinsider.py --format flac ano-natsu-de-matteru-op-single-sign
```

If you don't want to go to the actual site to look for soundtracks, you can also just type a search term as the first parameter(s), and provided it's not a valid soundtrack, `thehylia.py` will give you a list of soundtracks matching that term.

You're going to need [Python](https://www.python.org/downloads/) (if you don't know which version to get, choose the latest version of Python 3 - `thehylia.py` works with both 2 and 3), so install that (and [add it to your path](http://superuser.com/a/143121)) if you haven't already.

You will also need to have [pip](https://pip.readthedocs.org/en/latest/installing.html) installed (if you have Python 3, it is most likely already installed - otherwise, download `get-pip.py` and run it) if you don't already have [requests](https://pypi.python.org/pypi/requests) and [Beautiful Soup 4](https://pypi.python.org/pypi/beautifulsoup4). The first time `khinsider.py` runs, it will install these two for you.

For more detailed information, try running `thehylia.py --help`!

## As a module

`thehylia.py` requires two non-standard modules: [requests](https://pypi.python.org/pypi/requests) and [beautifulsoup4](https://pypi.python.org/pypi/beautifulsoup4). Just run a `pip install` on them (with [pip](https://pip.readthedocs.org/en/latest/installing.html)), or just run `thehylia.py` on its own once and it'll install them for you.

Here are the main functions you will be using:

### `thehylia.download(soundtrackName[, path="", makeDirs=True, formatOrder=None, verbose=False])`

Download the soundtrack `soundtrackName`. This should be the name the soundtrack uses at the end of its album URL.

If `path` is specified, the soundtrack files will be downloaded to the directory that path points to.

If `makeDirs` is `True`, the directory will be created if it doesn't exist.

You can specify `formatOrder` to download soundtracks in specific formats. `formatOrder=['flac', 'mp3']`, for example, will download FLACs if available, and MP3s if not.

If `verbose` is `True`, it will print progress as it is downloading.

### `thehylia.search(term)`

Search khinsider for `term`. Return a list of `Soundtrack`s matching the search term. You can then access `soundtrack.id` or `soundtrack.url`.

### More

There's a lot more detail to the API - more than would be sensible to write here. If you want to use `khinsider.py` as a module in a more advanced capacity, have a look at the `Soundtrack`, `Song`, and `File` objects in the source code! They're documented properly there for your reading pleasure.

# Is this `khinsider.py` except it's for The Hylia?

Yes. Yes, it is.

The creators of the sites were nice enough to use a very, very similar site structure, which made a The Hylia script not only very possible, but very easy (or, uh, it should've been, had I not gone all metaprogramming-y on it). It would absolutely be possible to have both in the same script, with an argument for which site to check / download from, but I feel the separation of them as two scripts is logical and easier to handle.

# Talk to me!

You can easily get to me in these ways:

* [@obskyr](http://twitter.com/obskyr/) on Twitter!
* [E-mail](mailto:powpowd@gmail.com) me!

I'd love to hear it if you like `thehylia.py`! If there's a problem, or you'd like a new feature, submit an issue here on GitHub.

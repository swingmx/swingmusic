import time
import schedule

from swingmusic.utils.threading import background

# IMPORTANT: `crons/__init__.py` is loaded transitively whenever anything
# imports `swingmusic.crons.cron` (which is where the CronJob base class
# lives). The recipe submodules — recents, topstreamed — inherit from
# CronJob, so they trigger that load path. If we also imported the
# recipes here at module level, we'd get a circular import: loading
# topstreamed → loads crons pkg → tries to import topstreamed again (mid-
# init) → ImportError. Keep this module's top-level imports minimal and
# defer recipe/premium imports into `start_cron_jobs`.


@background
def start_cron_jobs(and_exit: bool = False):
    """
    This is the function that triggers the cron jobs.
    """
    from swingmusic.lib.recipes.recents import RecentlyAdded, RecentlyPlayed
    from swingmusic.lib.recipes.topstreamed import TopArtists

    # Premium symbols are looked up via the module object at call time,
    # not captured via `from swingmusic.premium import X` at module-level.
    # The reason is identical to the recipe-import deferral above: during
    # premium.__init__ a partial `swingmusic.premium` module with the
    # free-tier stubs (None) exists briefly, and any `from swingmusic.premium
    # import X` evaluated against that partial module binds X to the stub
    # permanently. Attribute access via `premium.X` at call time always
    # sees the finalized values.
    import swingmusic.premium as premium

    # NOTE: RecentlyPlayed is not a CRON job, it's triggered here to
    # populate the values for the very first time.
    print("start_cron_jobs")
    RecentlyPlayed()
    RecentlyAdded()

    # Initialized CRON jobs
    TopArtists()
    TopArtists(duration="week")

    # Premium cron jobs are only registered when the compiled premium
    # modules are present in this build.
    if premium.MixesCron is not None:
        print("MixesCron is not None")
        premium.MixesCron()
    if premium.LicenseValidation is not None:
        print("LicenseValidation is not None")
        premium.LicenseValidation()

    # Trigger all CRON jobs when the app is started.
    schedule.run_all()

    # To manually trigger cron jobs, only once
    if and_exit:
        return

    # Run all CRON jobs on a loop.
    while True:
        schedule.run_pending()
        time.sleep(1)

import time
import schedule

from swingmusic.utils.threading import background


@background
def start_cron_jobs(and_exit: bool = False):
    """
    This is the function that triggers the cron jobs.
    """
    from swingmusic.lib.recipes.recents import RecentlyAdded, RecentlyPlayed
    from swingmusic.lib.recipes.topstreamed import TopArtists

    import swingmusic.premium as premium

    # NOTE: RecentlyPlayed is not a CRON job, it's triggered here to
    # populate the values for the very first time.
    RecentlyPlayed()
    RecentlyAdded()

    register = not and_exit

    jobs = [
        TopArtists(register=register),
        TopArtists(duration="week", register=register),
    ]

    # Premium cron jobs are only registered when the compiled premium
    # modules are present in this build.
    if premium.MixesCron is not None:
        jobs.append(premium.MixesCron(register=register))
    if premium.LicenseValidation is not None:
        jobs.append(premium.LicenseValidation(register=register))
    if premium.ClassicalSync is not None:
        jobs.append(premium.ClassicalSync(register=register))

    # Trigger all CRON jobs when the app is started.
    for job in jobs:
        job.run()

    # To manually trigger cron jobs, only once
    if and_exit:
        return

    # Run all CRON jobs on a loop.
    while True:
        schedule.run_pending()
        time.sleep(1)

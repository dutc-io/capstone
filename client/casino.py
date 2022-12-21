import asyncio

from json import dumps 
from logging import DEBUG, basicConfig, getLogger
from argparse import ArgumentParser

from httpx import HTTPError

from client_api import Casino, ENDPOINTS

logger = getLogger(__name__)
basicConfig(
    level=DEBUG,
    format="%(asctime)s %(levelname)s %(name)-10s %(message)s",
    datefmt="%d-%b %H:%M:%S",
)

def make_params(args):
    # XXX: Just for quick testing

    params = {}
    # Such close naming what could go wrong?
    if args.players:
        params['players'] = args.players
    if args.player:
        params['player'] = args.player

    if args.game:
        params['game'] = args.game

    if args.target:
        params['target'] = args.target
    if args.card:
        params['card'] = args.card
    if args.card:
        params['card'] = args.card

    return params

async def process(args):
    async with Casino.connect() as api:
        params = make_params(args)
        fn = getattr(api, ENDPOINTS[args.action])
        logger.debug(f"Action: {ENDPOINTS[args.action]}")
        logger.debug(f"Params: {params}")
        try:
            if params:
                results = await fn(params=dumps(params))
            else:
                results = await fn()
        except HTTPError as e:
            msg = f"HTTP Error @ {e.request.url}"
            logger.error(msg)
            results = {"status code": 404, "messge": f"{msg}"}
        except Exception as e:
            msg = f"Unknown Exception @ {e}"
            logger.error(msg)
            results = {"status code": 404, "messge": f"{msg}"}

    logger.info(results)


if __name__ == "__main__":
    parser = ArgumentParser(description="Casino")
    parser.add_argument(
        "action",
        choices=ENDPOINTS,
        help="The action you would like to take in the game",
    )
    parser.add_argument(
        "-target",
        default=None,
        type=int,
        help="# of the Card Target the action is preformed with",
    )
    parser.add_argument(
        "-game",
        default=None,
        help="Game the action is preformed with",
    )
    parser.add_argument(
        "-card",
        default=None,
        type=int,
        help="# of the Card the action is preformed with",
    )
    parser.add_argument(
        "-player",
        default=None,
        help="Player the action is preformed with",
    )
    parser.add_argument(
        "-players",
        default=None,
        nargs="+",
        help="Players to start the game with",
    )

    args = parser.parse_args()
    asyncio.run(process(args))

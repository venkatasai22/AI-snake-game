import argparse
from trainer import train, play_human


def main():
    parser = argparse.ArgumentParser(description='AI Snake Game')
    parser.add_argument('--mode', choices=['human', 'train'], default='human', help='human to play or train AI')
    parser.add_argument('--episodes', type=int, default=500, help='training episodes')
    args = parser.parse_args()

    if args.mode == 'human':
        play_human()
    elif args.mode == 'train':
        train(episodes=args.episodes)


if __name__ == '__main__':
    main()

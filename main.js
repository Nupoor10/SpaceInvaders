import MenuScene from './MenuScene.js';
import GameScene from './GameScene.js';

const config = {
    type: Phaser.AUTO,
    width: 1000,
    height: 750,
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    },
    physics: {
        default: 'arcade',
        arcade: { debug: false }
    },
    // Both scenes are imported and registered here
    scene: [MenuScene, GameScene]
};

const game = new Phaser.Game(config);

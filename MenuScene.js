export default class MenuScene extends Phaser.Scene {
    constructor() {
        super('MenuScene');
    }

    preload() {
        this.load.image('bg', 'assets/background-black.png');
        this.load.image('player', 'assets/pixel_ship_yellow.png');
        this.load.image('laserYellow', 'assets/pixel_laser_yellow.png');
        this.load.image('enemyRed', 'assets/pixel_ship_red_small.png');
        this.load.image('enemyGreen', 'assets/pixel_ship_green_small.png');
        this.load.image('enemyBlue', 'assets/pixel_ship_blue_small.png');
        this.load.image('powerUp', 'assets/pixel_laser_green.png');
        this.load.image('powerUpHealth', 'assets/pixel_laser_red.png');

        this.load.audio('bgMusic', 'assets/bgMusic.mp3');
        this.load.audio('shoot', 'assets/shoot.wav');
    }

    create() {
        this.background = this.add.tileSprite(500, 375, 1000, 750, 'bg');

        this.add.text(500, 200, 'PIXEL SIEGE', { fontSize: '64px', fill: '#0ff', fontFamily: 'Courier', fontStyle: 'bold' }).setOrigin(0.5);
        const startText = this.add.text(500, 420, 'CLICK OR PRESS ENTER TO START', { fontSize: '32px', fill: '#ff0', fontFamily: 'Courier' }).setOrigin(0.5);

        this.tweens.add({ targets: startText, alpha: 0, duration: 600, yoyo: true, repeat: -1 });

        const rules = "HOW TO PLAY\n[ ARROW KEYS ] - Move Ship\n[ SPACEBAR ] - Fire Lasers\n\n- GREEN drops upgrade to Double Lasers!\n- RED drops restore 20 Health!\n- Blue = 10 pts | Green = 20 pts | Red = 50 pts";
        this.add.text(500, 580, rules, { fontSize: '20px', fill: '#fff', fontFamily: 'Courier', align: 'center', lineSpacing: 10 }).setOrigin(0.5);

        this.bgMusic = this.sound.add('bgMusic', { loop: true, volume: 0.5 });
        this.bgMusic.play();

        this.input.keyboard.once('keydown-ENTER', () => {
            this.bgMusic.stop();
            this.scene.start('GameScene');
        });

        this.input.once('pointerdown', () => {
            this.bgMusic.stop();
            this.scene.start('GameScene');
        });
    }
    update() {
        this.background.tilePositionY -= 2;
    }
}

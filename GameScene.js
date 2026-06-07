export default class GameScene extends Phaser.Scene {
    constructor() {
        super('GameScene');
    }

    create() {
        // Class-scoped state variables
        this.isGameOver = false;
        this.score = 0;
        this.level = 1;
        this.waveLength = 5;
        this.wavesSpawned = 0;
        this.playerHealth = 100;
        this.hasDoubleLaser = false;
        this.lastFired = 0;
        this.highScore = localStorage.getItem('spaceInvadersHighScore') || 0;

        this.background = this.add.tileSprite(500, 375, 1000, 750, 'bg');

        this.player = this.physics.add.sprite(500, 630, 'player');
        this.player.setCollideWorldBounds(true);

        this.cursors = this.input.keyboard.createCursorKeys();

        // Physics groups
        this.playerLasers = this.physics.add.group();
        this.enemies = this.physics.add.group();
        this.powerUps = this.physics.add.group();
        this.healthPowerUps = this.physics.add.group();

        // Collisions mapped to class methods
        this.physics.add.overlap(this.playerLasers, this.enemies, this.hitEnemy, null, this);
        this.physics.add.overlap(this.player, this.enemies, this.hitPlayer, null, this);
        this.physics.add.overlap(this.player, this.powerUps, this.collectPowerUp, null, this);
        this.physics.add.overlap(this.player, this.healthPowerUps, this.collectHealth, null, this);

        // UI
        this.scoreText = this.add.text(20, 20, 'SCORE: 0', { fontSize: '24px', fill: '#fff', fontFamily: 'Courier' });
        this.levelText = this.add.text(20, 50, 'LEVEL: 1', { fontSize: '24px', fill: '#fff', fontFamily: 'Courier' });
        this.highScoreText = this.add.text(750, 20, `HI-SCORE: ${this.highScore}`, { fontSize: '24px', fill: '#ff0', fontFamily: 'Courier' });

        this.healthBar = this.add.graphics();

        this.waveEvent = this.time.addEvent({ delay: 5000, callback: this.spawnWave, callbackScope: this, loop: true });
        this.spawnWave();
        this.events.on('postupdate', this.drawHealthBar, this);
    }

    update(time, delta) {
        if (this.isGameOver) return;

        this.background.tilePositionY -= 2;

        this.player.setVelocity(0);
        if (this.cursors.left.isDown) this.player.setVelocityX(-350);
        else if (this.cursors.right.isDown) this.player.setVelocityX(350);

        if (this.cursors.up.isDown) this.player.setVelocityY(-350);
        else if (this.cursors.down.isDown) this.player.setVelocityY(350);

        if (this.cursors.space.isDown && time > this.lastFired) {
            if (this.hasDoubleLaser) {
                const laser1 = this.playerLasers.create(this.player.x - 15, this.player.y - 30, 'laserYellow');
                const laser2 = this.playerLasers.create(this.player.x + 15, this.player.y - 30, 'laserYellow');
                laser1.setVelocityY(-800);
                laser2.setVelocityY(-800);
            } else {
                const laser = this.playerLasers.create(this.player.x, this.player.y - 30, 'laserYellow');
                laser.setVelocityY(-800);
            }
            this.lastFired = time + 150;

            this.sound.play('shoot', { volume: 0.3 });
        }

        this.playerLasers.getChildren().forEach(laser => { if (laser.active && laser.y < 0) laser.destroy(); });
        this.enemies.getChildren().forEach(enemy => { if (enemy.active && enemy.y > 800) enemy.destroy(); });
        this.powerUps.getChildren().forEach(pu => { if (pu.active && pu.y > 800) pu.destroy(); });
        this.healthPowerUps.getChildren().forEach(pu => { if (pu.active && pu.y > 800) pu.destroy(); });
    }

    drawHealthBar() {
        this.healthBar.clear();
        if (this.playerHealth > 0) {
            this.healthBar.fillStyle(0xff0000);
            this.healthBar.fillRect(this.player.x - 25, this.player.y + 40, 50, 10);

            this.healthBar.fillStyle(0x00ff00);
            this.healthBar.fillRect(this.player.x - 25, this.player.y + 40, 50 * (this.playerHealth / 100), 10);
        }
    }

    hitEnemy(laser, enemy) {
        laser.destroy();
        let health = enemy.getData('health') - 1;
        enemy.setData('health', health);

        if (health <= 0) {
            const type = enemy.getData('type');
            let pointsAdded = 0;

            if (type === 'Blue') pointsAdded = 10;
            else if (type === 'Green') pointsAdded = 20;
            else if (type === 'Red') pointsAdded = 50;

            this.score += pointsAdded;
            this.scoreText.setText(`SCORE: ${this.score}`);

            const floatText = this.add.text(enemy.x, enemy.y, `+${pointsAdded}`, {
                fontSize: '20px', fill: '#00ff00', fontFamily: 'Courier', fontStyle: 'bold'
            }).setOrigin(0.5);

            this.tweens.add({ targets: floatText, y: enemy.y - 50, alpha: 0, duration: 1000, ease: 'Power1', onComplete: () => floatText.destroy() });

            const emitter = this.add.particles(enemy.x, enemy.y, 'laserYellow', {
                speed: { min: 50, max: 200 }, scale: { start: 0.5, end: 0 }, lifespan: 300, emitting: false
            });
            emitter.explode(15);

            if (Phaser.Math.Between(1, 100) <= 10) {
                const isHealthDrop = Phaser.Math.Between(0, 1) === 1;
                if (isHealthDrop) {
                    const pu = this.healthPowerUps.create(enemy.x, enemy.y, 'powerUpHealth');
                    pu.setVelocityY(150);
                } else {
                    const pu = this.powerUps.create(enemy.x, enemy.y, 'powerUp');
                    pu.setVelocityY(150);
                }
            }
            enemy.destroy();
        }
    }

    hitPlayer(playerShip, enemy) {
        enemy.destroy();
        this.playerHealth -= 20;

        this.cameras.main.shake(200, 0.01);
        this.cameras.main.flash(200, 255, 0, 0);
        this.hasDoubleLaser = false;

        if (this.playerHealth <= 0) {
            this.gameOver();
        }
    }

    collectPowerUp(playerShip, powerUp) {
        powerUp.destroy();
        this.hasDoubleLaser = true;
    }

    collectHealth(playerShip, healthDrop) {
        healthDrop.destroy();
        this.playerHealth += 20;
        if (this.playerHealth > 100) this.playerHealth = 100;

        const healText = this.add.text(playerShip.x, playerShip.y - 30, '+20 HP', {
            fontSize: '20px', fill: '#00ff00', fontFamily: 'Courier', fontStyle: 'bold'
        }).setOrigin(0.5);

        this.tweens.add({ targets: healText, y: playerShip.y - 80, alpha: 0, duration: 1000, ease: 'Power1', onComplete: () => healText.destroy() });
    }

    spawnWave() {
        if (this.isGameOver) return;

        let allowedTypes = [];
        if (this.level === 1) allowedTypes = ['Blue'];
        else if (this.level === 2) allowedTypes = ['Green'];
        else if (this.level === 3) allowedTypes = ['Blue', 'Green'];
        else if (this.level === 4) allowedTypes = ['Red'];
        else allowedTypes = ['Blue', 'Green', 'Red'];

        for (let i = 0; i < this.waveLength; i++) {
            this.time.delayedCall(i * 250, () => {
                if (this.isGameOver) return;

                const x = Phaser.Math.Between(50, 950);
                const type = Phaser.Math.RND.pick(allowedTypes);
                const enemy = this.enemies.create(x, -50, `enemy${type}`);
                enemy.setData('type', type);

                if (type === 'Blue') {
                    enemy.setData('health', 1);
                    enemy.setVelocityY(150);
                } else if (type === 'Green') {
                    enemy.setData('health', 1);
                    enemy.setVelocityY(100);
                    this.tweens.add({ targets: enemy, x: enemy.x + 100, duration: 1000, yoyo: true, repeat: -1, ease: 'Sine.easeInOut' });
                } else if (type === 'Red') {
                    enemy.setData('health', 2);
                    this.tweens.add({
                        targets: enemy, y: 200, duration: 1500, ease: 'Power1',
                        onComplete: () => {
                            if (enemy && enemy.active) {
                                const direction = enemy.x > 500 ? -350 : 350;
                                enemy.setVelocity(direction, 450);
                            }
                        }
                    });
                }
            });
        }

        this.wavesSpawned++;
        if (this.wavesSpawned % 4 === 0) {
            this.level++;
            this.levelText.setText(`LEVEL: ${this.level}`);
        }
        this.waveLength += 1;
    }

    gameOver() {
        this.isGameOver = true;
        this.physics.pause();
        this.waveEvent.remove();
        this.healthBar.clear();
        this.player.setTint(0xff0000);

        if (this.score > this.highScore) {
            this.highScore = this.score;
            localStorage.setItem('spaceInvadersHighScore', this.highScore);
        }

        this.add.text(500, 350, 'GAME OVER', { fontSize: '64px', fill: '#fff', fontFamily: 'Courier' }).setOrigin(0.5);
        this.add.text(500, 420, 'CLICK TO RESTART', { fontSize: '32px', fill: '#ff0', fontFamily: 'Courier' }).setOrigin(0.5);

        this.input.once('pointerdown', () => {
            this.scene.restart();
        });
    }
}

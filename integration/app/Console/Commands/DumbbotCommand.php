<?php

namespace App\Console\Commands;

use App\Utility\GameService;
use Illuminate\Console\Command;

class DumbbotCommand extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'dnw:dumbsingle {--max=50} {--dumb=} {--random=}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command description';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {
        $game = new GameService('dumbsingle');
        $game->initGame();
        $game->saveImgFiles();
        $i = 0;
        $dumb = array_filter(explode(',', $this->option('dumb')));
        $rand = array_filter(explode(',', $this->option('random')));
        $max = $this->option('max');
        $bar = $this->output->createProgressBar($max);
        $bar->start();
        while (!$game->isCompleted() && $i <= $max) {
            foreach ($dumb as $power) {
                $game->assignDumbbotOrders($power);
            }

            foreach ($rand as $power) {
                $game->assignRandomOrders($power);
            }
            $game->adjudicate();
            $game->saveImgFiles();
            $i++;
            $bar->advance();
        }
        $bar->finish();
    }
}

<?php

namespace App\Console\Commands;

use App\Utility\GameService;
use Illuminate\Console\Command;

class RandomCommands extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'dnw:random {--max=50}';

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

    public function handle()
    {
        $game = new GameService('random', 'standard');
        $game->initGame();
        $game->saveImgFiles();
        $i = 0;
        $max = $this->option('max');
        $bar = $this->output->createProgressBar($max);
        $bar->start();
        while(!$game->isCompleted() && $i <= $max){
            // $game->assignRandomOrders();
           $game->assignDumbbotOrders("FRANCE");
            $game->adjudicate();
            $game->saveImgFiles();
            $i++;
            $bar->advance();
        }
        $bar->finish();

    }
}

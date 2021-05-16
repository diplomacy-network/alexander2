<?php

namespace Tests;

use Illuminate\Support\Facades\Storage;
use Imagick;
use Symfony\Component\Yaml\Yaml;
use Illuminate\Foundation\Testing\TestCase as BaseTestCase;
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Support\Facades\Http;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    public PendingRequest $client;
    protected string $basePath;


    protected function setUp(): void
    {
        parent::setUp();
        $this->client = Http::baseUrl(env('API_BASE_URL'));

    }

    protected function executeTestRun(string $variant, string $runFile, string $phrase, int $scs_to_win): array
    {
        $path = Storage::path("instructions/$runFile");
        $orders = Yaml::parseFile($path);

        $currentTime = now()->toDateTimeLocalString();
        $this->basePath = 'img/'.$phrase.'/'.$currentTime;

        $i = 0;
        // Initialize
        $response = $this->client->get('/adjudicate/'.$variant);
        $data = $response->json();
        $previousPhaseName = $data['phase_short'];
        $currentPhaseName = $data['phase_short'];

        $this->saveImgFiles($i, $data, false, $currentPhaseName, $previousPhaseName);

        $encodedState = $data['current_state_encoded'];
        foreach ($orders as $orderBatch) {
            $i++;
            $instr = $orderBatch == "NONE" ? (object)[] : $orderBatch;

            $response = $this->client->post('adjudicate', [
                'previous_state_encoded' => $encodedState,
                'orders' => $instr,
                'scs_to_win' => $scs_to_win,
            ]);
            $data = $response->json();


            $currentPhaseName = $response->json('phase_short');
            $this->saveImgFiles($i, $data, true, $currentPhaseName, $previousPhaseName);

            if(str_contains($currentPhaseName, "COMPLETED")){
                break;
            }


            $previousPhaseName = $currentPhaseName;
            $encodedState = $data['current_state_encoded'];
        }

        return $data;
    }

    protected function saveImgFiles(int $index, array $data, bool $with_orders, string $currentPhase, string $previousPhase)
    {


        $baseAdjudicatedPath = "{$this->basePath}/{$index}_{$currentPhase}_0_adjudicated";
        $svgAdjudicated = $data['svg_adjudicated'];
        Storage::put("$baseAdjudicatedPath.svg", $svgAdjudicated);


        if ($with_orders) {
            $previousIndex = $index-1;
            $baseWithOrdersPath = "{$this->basePath}/{$previousIndex}_{$previousPhase}_1_with_orders";
            $svgWithOrders = $data['svg_with_orders'];
            Storage::put("$baseWithOrdersPath.svg", $svgWithOrders);
        }

    }


}

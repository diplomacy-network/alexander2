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

    protected function executeTestRun(string $variant, string $runFile, string $phrase): array
    {
        $path = Storage::path("instructions/$runFile");
        $orders = Yaml::parseFile($path);

        $currentTime = now()->toDateTimeLocalString();
        $this->basePath = 'img/'.$phrase.'/'.$currentTime;

        $i = 0;
        // Initialize
        $response = $this->client->get('/adjudicate/'.$variant);
        $data = $response->json();
        $this->saveImgFiles($i, $data, false);

        $encodedState = $data['current_state_encoded'];
        foreach ($orders as $orderBatch) {
            $i++;
            $instr = [];
            if ($orderBatch != "NONE") {

                foreach ($orderBatch as $power => $instructions) {
                    $instr[] = [
                        'power' => $power,
                        'instructions' => $instructions,
                    ];
                }
            }
            $response = $this->client->post('adjudicate', [
                'previous_state_encoded' => $encodedState,
                'orders' => $instr,
            ]);
            $data = $response->json();
            $this->saveImgFiles($i, $data, true);
            $encodedState = $data['current_state_encoded'];
        }

        return $data;
    }

    protected function saveImgFiles(int $index, array $data, bool $with_orders)
    {


        $baseAdjudicatedPath = "{$this->basePath}/{$index}_{$data['phase']}_1_adjudicated";
        $svgAdjudicated = $data['svg_adjudicated'];
        Storage::put("$baseAdjudicatedPath.svg", $svgAdjudicated);


        if ($with_orders) {
            $baseWithOrdersPath = "{$this->basePath}/{$index}_{$data['phase']}_0_with_orders";
            $svgWithOrders = $data['svg_with_orders'];
            Storage::put("$baseWithOrdersPath.svg", $svgWithOrders);
        }

    }


}

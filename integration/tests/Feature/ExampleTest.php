<?php

namespace Tests\Feature;

use Helmich\JsonAssert\JsonAssertions;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use JsonAssertions;

    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_example()
    {
        $response = $this->client->get('variants');
        $this->assertJsonValueEquals($response->body(), '$.*.name', 'standard');

    }
}

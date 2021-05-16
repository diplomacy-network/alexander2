<?php

namespace Tests\Feature;

use Helmich\JsonAssert\JsonAssertions;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

class WinnerTest extends TestCase
{
    use JsonAssertions;

    /** @test */
    public function custom_number_of_supply_centers(){
        $result = $this->executeTestRun('standard', 'base.yaml', 'custom_number_of_supply_centers', 5);

        $this->assertJsonValueEquals($result, 'winners[0]', "FRANCE");
    }
}

<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

class BasicTestRunGenerationTest extends TestCase
{

    /** @test */
    public function basic_test_run_generation(){
        $this->executeTestRun('standard', 'base.yaml', 'base', 18);

    }
}

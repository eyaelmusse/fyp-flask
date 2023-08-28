/*
 * This file was automatically generated by EvoSuite
 * Mon Aug 28 01:55:57 GMT 2023
 */

package net.kencochrane.a4j.beans;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.ArrayList;
import net.kencochrane.a4j.beans.FullProduct;
import net.kencochrane.a4j.beans.MiniProduct;
import net.kencochrane.a4j.beans.ProductDetails;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class FullProduct_ESTest extends FullProduct_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      fullProduct0.setSimilarItems((ArrayList) null);
      fullProduct0.printFullProduct();
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      ArrayList<Integer> arrayList0 = new ArrayList<Integer>();
      fullProduct0.accessories = arrayList0;
      Integer integer0 = new Integer((-4415));
      arrayList0.add(integer0);
      fullProduct0.printFullProduct();
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      fullProduct0.setAccessories((ArrayList) null);
      fullProduct0.printFullProduct();
  }

  @Test(timeout = 4000)
  public void test3()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      ProductDetails productDetails0 = fullProduct0.getDetails();
      assertNull(productDetails0.getSalesRank());
  }

  @Test(timeout = 4000)
  public void test4()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      MiniProduct miniProduct0 = new MiniProduct();
      fullProduct0.addAccessory(miniProduct0);
      assertNull(miniProduct0.getProductUrl());
  }

  @Test(timeout = 4000)
  public void test5()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      ProductDetails productDetails0 = fullProduct0.details;
      fullProduct0.setDetails(productDetails0);
      assertNull(productDetails0.getEsrbRating());
  }

  @Test(timeout = 4000)
  public void test6()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      ArrayList arrayList0 = fullProduct0.getAccessories();
      assertTrue(arrayList0.isEmpty());
  }

  @Test(timeout = 4000)
  public void test7()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      MiniProduct miniProduct0 = new MiniProduct();
      fullProduct0.addSimilarItem(miniProduct0);
      fullProduct0.printFullProduct();
  }

  @Test(timeout = 4000)
  public void test8()  throws Throwable  {
      FullProduct fullProduct0 = new FullProduct();
      ArrayList arrayList0 = fullProduct0.getSimilarItems();
      assertEquals(0, arrayList0.size());
  }
}
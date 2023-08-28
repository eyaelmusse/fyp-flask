/*
 * This file was automatically generated by EvoSuite
 * Mon Aug 28 02:08:46 GMT 2023
 */

package net.kencochrane.a4j.data;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import java.util.ArrayList;
import net.kencochrane.a4j.data.Query;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.evosuite.runtime.testdata.EvoSuiteURL;
import org.evosuite.runtime.testdata.NetworkHandling;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class Query_ESTest extends Query_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test00()  throws Throwable  {
      Query query0 = new Query();
      EvoSuiteURL evoSuiteURL0 = new EvoSuiteURL("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&BlendedSearch=h%3FF%27%40&type=null&f=xml");
      NetworkHandling.createRemoteTextFile(evoSuiteURL0, "^dKa@pCAJ\"4V");
      String string0 = query0.sendRequest("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&BlendedSearch=h%3FF%27%40&type=null&f=xml");
      assertEquals("^dKa@pCAJ\"4V", string0);
  }

  @Test(timeout = 4000)
  public void test01()  throws Throwable  {
      Query query0 = new Query();
      ArrayList<Integer> arrayList0 = new ArrayList<Integer>();
      Integer integer0 = new Integer((-4421));
      arrayList0.add(integer0);
      arrayList0.add(integer0);
      String string0 = query0.queryGenerator("AsinSearch", "", "AsinSearch", "", arrayList0);
      assertEquals("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&AsinSearch=-4421,-4421&type=&offerpage=AsinSearch&offer=&f=xml", string0);
  }

  @Test(timeout = 4000)
  public void test02()  throws Throwable  {
      Query query0 = new Query();
      // Undeclared exception!
      try { 
        query0.queryGenerator("AsinSearch", "T", "AsinSearch", "T", (ArrayList) null);
        fail("Expecting exception: NullPointerException");
      
      } catch(NullPointerException e) {
         //
         // no message in exception (getMessage() returned null)
         //
         verifyException("net.kencochrane.a4j.data.Query", e);
      }
  }

  @Test(timeout = 4000)
  public void test03()  throws Throwable  {
      Query query0 = new Query();
      ArrayList<Integer> arrayList0 = new ArrayList<Integer>();
      // Undeclared exception!
      try { 
        query0.queryGenerator("AsinSearch", "", "AsinSearch", "", arrayList0);
        fail("Expecting exception: IndexOutOfBoundsException");
      
      } catch(IndexOutOfBoundsException e) {
         //
         // Index: 0, Size: 0
         //
         verifyException("java.util.ArrayList", e);
      }
  }

  @Test(timeout = 4000)
  public void test04()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.RemoveFromCart("-", "-", "");
      assertEquals("http://xml.amazon.net/onca/xml3?ShoppingCart=remove&f=xml&dev-t=DSB0XDDW1GQ3S&t=popcornmonste2-20&Item.-&CartId=-&Hmac=", string0);
  }

  @Test(timeout = 4000)
  public void test05()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.GetItemsFromCart("\"4{]+", "\"4{]+");
      assertEquals("http://xml.amazon.net/onca/xml3?ShoppingCart=get&f=xml&dev-t=DSB0XDDW1GQ3S&t=popcornmonste2-20&CartId=\"4{]+&Hmac=%224%7B%5D%2B", string0);
  }

  @Test(timeout = 4000)
  public void test06()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.AddToExistingCart("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&KeywordSearch=&mode=AsinSearch&type=AsinSearch&page=AsinSearch&f=xml", "", "http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&AsinSearch=-4421&type=&offerpage=AsinSearch&offer=&f=xml", "K`d0\"(");
      assertEquals("http://xml.amazon.net/onca/xml3?ShoppingCart=add&f=xml&dev-t=DSB0XDDW1GQ3S&t=popcornmonste2-20&Asin.http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&KeywordSearch=&mode=AsinSearch&type=AsinSearch&page=AsinSearch&f=xml=&CartId=http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&AsinSearch=-4421&type=&offerpage=AsinSearch&offer=&f=xml&Hmac=K%60d0%22%28", string0);
  }

  @Test(timeout = 4000)
  public void test07()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.ModifyCart("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&AsinSearch=-4421&type=&offerpage=AsinSearch&offer=&f=xml", "AsinSearch", "http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&AsinSearch=-4421&type=&offerpage=AsinSearch&offer=&f=xml", "http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&KeywordSearch=&mode=AsinSearch&type=AsinSearch&page=AsinSearch&f=xml");
      assertEquals("http://xml.amazon.net/onca/xml3?ShoppingCart=modify&f=xml&dev-t=DSB0XDDW1GQ3S&t=popcornmonste2-20&Item.http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&AsinSearch=-4421&type=&offerpage=AsinSearch&offer=&f=xml=AsinSearch&CartId=http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&AsinSearch=-4421&type=&offerpage=AsinSearch&offer=&f=xml&Hmac=http%3A%2F%2Fxml.amazon.net%2Fonca%2Fxml3%3Ft%3Dpopcornmonste2-20%26dev-t%3DDSB0XDDW1GQ3S%26KeywordSearch%3D%26mode%3DAsinSearch%26type%3DAsinSearch%26page%3DAsinSearch%26f%3Dxml", string0);
  }

  @Test(timeout = 4000)
  public void test08()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.ClearCart("BAHvRx].6~H!7g", "BAHvRx].6~H!7g");
      assertEquals("http://xml.amazon.net/onca/xml3?ShoppingCart=clear&f=xml&dev-t=DSB0XDDW1GQ3S&t=popcornmonste2-20&CartId=BAHvRx].6~H!7g&Hmac=BAHvRx%5D.6%7EH%217g", string0);
  }

  @Test(timeout = 4000)
  public void test09()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.SearchThirdPartyGenerator("", "UTF-8", "7l3", "UTF-8");
      assertEquals("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&SellerSearch=&type=UTF-8&page=7l3&offerstatus=UTF-8&f=xml", string0);
  }

  @Test(timeout = 4000)
  public void test10()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.browseNodeQueryGenerator("rNS!A", "", "Dbjl. \"Ge", ">'[kv!acgt!S", "Dbjl. \"Ge");
      assertEquals("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&BrowseNodeSearch=Dbjl. \"Ge&mode=>'[kv!acgt!S&type=rNS!A&page=&offer=Dbjl. \"Ge&f=xml", string0);
  }

  @Test(timeout = 4000)
  public void test11()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.KeywordSearchGenerator("", "AsinSearch", "AsinSearch", "AsinSearch");
      assertEquals("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&KeywordSearch=&mode=AsinSearch&type=AsinSearch&page=AsinSearch&f=xml", string0);
  }

  @Test(timeout = 4000)
  public void test12()  throws Throwable  {
      Query query0 = new Query();
      ArrayList<Object> arrayList0 = new ArrayList<Object>();
      // Undeclared exception!
      try { 
        query0.queryGenerator("^dKa@pCAJ\"4V", "http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&SellerSearch=&type=UTF-8&page=7l3&offerstatus=UTF-8&f=xml", "http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&BlendedSearch=h%3FF%27%40&type=null&f=xml", "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-~|+", arrayList0);
        fail("Expecting exception: IndexOutOfBoundsException");
      
      } catch(IndexOutOfBoundsException e) {
         //
         // Index: 0, Size: 0
         //
         verifyException("java.util.ArrayList", e);
      }
  }

  @Test(timeout = 4000)
  public void test13()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.AddtoCart("WeSs", "O|{!g# }yft");
      assertEquals("http://xml.amazon.net/onca/xml3?ShoppingCart=add&f=xml&dev-t=DSB0XDDW1GQ3S&t=popcornmonste2-20&Asin.WeSs=O|{!g# }yft", string0);
  }

  @Test(timeout = 4000)
  public void test14()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.SearchQueryGenerator("1,`6ZBf", "1,`6ZBf", "1,`6ZBf", "0W yi", "84PDpesu(pK*?q}", "84PDpesu(pK*?q}");
      assertEquals("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&1,`6ZBf=1%2C%606ZBf&mode=1,`6ZBf&type=0W yi&page=84PDpesu(pK*?q}&offer=84PDpesu(pK*?q}&f=xml", string0);
  }

  @Test(timeout = 4000)
  public void test15()  throws Throwable  {
      Query query0 = new Query();
      String string0 = query0.BlendedSearchGenerator((String) null, "h?F'@");
      assertEquals("http://xml.amazon.net/onca/xml3?t=popcornmonste2-20&dev-t=DSB0XDDW1GQ3S&BlendedSearch=h%3FF%27%40&type=null&f=xml", string0);
  }
}
